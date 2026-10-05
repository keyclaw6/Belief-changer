"""Owned Clearcote research browser and private, portable authenticated state.

No model calls. Optional browser/crypto dependencies are loaded only for live use.
"""
from __future__ import annotations

import importlib.metadata
import json
import os
import secrets
import select
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from .common import FactoryError, atomic_bytes, lock, read_json, require

UNIT = "belief-changer-research-browser.service"


def settings(repo: Path) -> tuple[dict, Path]:
    from .research_access import config, state_root
    c = config(repo)
    require(c.get("browser_engine") == "clearcote", "Configure the reviewed Clearcote research engine")
    return c, state_root(repo, True)


def private_file(path: Path, repo: Path, *, existing: bool = False) -> Path:
    path = path.expanduser().absolute()
    require(not any(p.is_symlink() for p in (path, *path.parents)), "Authentication paths must not be symlinks")
    path = path.resolve()
    require(not path.is_relative_to(repo.resolve()), "Authentication files must remain outside the repository")
    if existing:
        require(path.is_file(), "Required private authentication file is missing")
        if os.name == "posix":
            st = path.stat()
            require(st.st_uid == os.getuid() and st.st_mode & 0o077 == 0,
                    "Authentication files must be owner-only (0600)")
    return path


def write_private(path: Path, data: bytes, repo: Path) -> None:
    path = private_file(path, repo)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    atomic_bytes(path, data)
    if os.name == "posix":
        path.chmod(0o600)


def cipher(repo: Path, home: Path, *, create: bool = False):
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        raise FactoryError("Install the pinned research dependencies with research-bootstrap --apply") from None
    key = home / "auth/transfer.key"
    if not key.exists():
        require(create and not (home / "auth/state.enc").exists(),
                "Restore the existing private transfer key; never replace it to bypass a failed import")
        write_private(key, Fernet.generate_key(), repo)
    try:
        return Fernet(private_file(key, repo, existing=True).read_bytes())
    except ValueError:
        raise FactoryError("Invalid private browser-state transfer key") from None


def environment(home: Path) -> dict:
    env = os.environ.copy()
    env["CLEARCOTE_CACHE"] = str(home / "clearcote-cache")
    return env


def endpoint(c: dict) -> str:
    return "http://127.0.0.1:" + str(c["browser_port"])


def cdp_version(c: dict) -> dict | None:
    try:
        with urllib.request.urlopen(endpoint(c) + "/json/version", timeout=3) as r:
            return json.load(r)
    except (OSError, ValueError):
        return None


def bridge_profiles() -> set[str]:
    try:
        request = urllib.request.Request('http://127.0.0.1:19825/status', headers={'X-OpenCLI':'belief-changer'})
        with urllib.request.urlopen(request, timeout=3) as r:
            data = json.load(r)
        return {p['contextId'] for p in data.get('profiles', []) if p.get('contextId') and p.get('extensionConnected') is True}
    except (OSError, ValueError, KeyError):
        return set()


def owned_bridge(c: dict, home: Path) -> str | None:
    argv=['node',str(Path(__file__).with_name('research_state.cjs')),'bridge-id',endpoint(c),
          str(home/'node/node_modules/playwright-core'),json.dumps(c['auth_domains'])]
    try: result=subprocess.run(argv,capture_output=True,timeout=15)
    except (OSError,subprocess.TimeoutExpired): return None
    if result.returncode: return None
    try: identity=json.loads(result.stdout)
    except ValueError: return None
    return identity.get('contextId') if identity.get('version')==c['opencli_extension_version'] else None


def bind_bridge(c: dict, home: Path, previous: set[str]) -> str:
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        profiles = bridge_profiles()
        selected = owned_bridge(c,home)
        if selected not in profiles: selected = None
        if selected:
            env = environment(home)
            env['OPENCLI_CONFIG_DIR'] = str(home / 'opencli-config')
            for alias in set(c.get('bridge_profiles', {}).values()) | {c['bridge_profile']}:
                args = [str(home / 'node/node_modules/.bin/opencli'), 'profile', 'rename', selected, alias]
                result = subprocess.run(args, env=env, capture_output=True, timeout=15)
                require(result.returncode == 0, 'Could not bind the owned research Browser Bridge profile')
            return selected
        time.sleep(.2)
    raise FactoryError('Owned Browser Bridge did not register uniquely; inspect its endpoint/extension')


def transfer(repo: Path, direction: str, *, source: str | None = None) -> dict:
    c, home = settings(repo)
    url = source or endpoint(c)
    require(url == endpoint(c), "State transfer is limited to the selected research CDP endpoint")
    helper = Path(__file__).with_name("research_state.cjs")
    args = ["node", str(helper), direction, url, str(home / "node/node_modules/playwright-core"),
            json.dumps(c["auth_domains"])]
    if direction == "import":
        state_path = private_file(home / "auth/state.enc", repo, existing=True)
        try:
            plaintext = cipher(repo, home).decrypt(state_path.read_bytes())
        except Exception:
            raise FactoryError("Browser-state authentication/decryption failed; no state imported") from None
    else:
        plaintext = None
    result = subprocess.run(args, input=plaintext, capture_output=True, timeout=60)
    require(result.returncode == 0, "Browser-state transfer failed; credential-bearing diagnostics suppressed")
    if direction == "export":
        try:
            state = json.loads(result.stdout)
        except ValueError:
            raise FactoryError("Browser-state exporter returned invalid data") from None
        seed = home / "fingerprint-seed"
        if not seed.exists():
            write_private(seed, ("belief-changer-" + secrets.token_hex(16) + "\n").encode(), repo)
        state["fingerprint"] = seed.read_text().strip()
        encrypted = cipher(repo, home, create=True).encrypt(json.dumps(state).encode())
        write_private(home / "auth/state.enc", encrypted, repo)
        return {"operation": "export", "encrypted": True,
                "cookies": len(state["state"].get("cookies", [])),
                "origins": len(state["state"].get("origins", []))}
    return {"operation": "import", "authenticated_bundle": True}


def portable(repo: Path, direction: str, bundle: Path, key: Path | None = None) -> dict:
    _, home = settings(repo)
    bundle = private_file(bundle, repo, existing=direction == "import")
    if direction == "export":
        require((home / "auth/state.enc").is_file(), "Export live browser state before making a portable bundle")
        write_private(bundle, (home / "auth/state.enc").read_bytes(), repo)
        return {"operation": "portable-export", "path": str(bundle),
                "key_required_separately": str(home / "auth/transfer.key")}
    require(key is not None, "Supply the separately transferred private key file")
    key = private_file(key, repo, existing=True)
    try:
        from cryptography.fernet import Fernet
        restored = json.loads(Fernet(key.read_bytes()).decrypt(bundle.read_bytes()))
    except Exception:
        raise FactoryError("Portable browser bundle/key validation failed; nothing installed") from None
    require(not cdp_version(settings(repo)[0]), "Stop the owned research browser before installing portable state")
    require(isinstance(restored.get("fingerprint"), str) and bool(restored["fingerprint"]),
            "Portable state is missing its stable browser identity")
    require(restored.get('version') == 1 and isinstance(restored.get('state'), dict)
            and isinstance(restored['state'].get('cookies'), list)
            and isinstance(restored['state'].get('origins'), list)
            and isinstance(restored.get('sessions', {}), dict), 'Portable state has an invalid storage schema')
    current_key = home / 'auth/transfer.key'
    if (home/'auth/state.enc').exists() and current_key.exists():
        require(current_key.read_bytes() == key.read_bytes(),
                'Preserve existing auth state: restore another key into a fresh external research home')
    write_private(home / "auth/transfer.key", key.read_bytes(), repo)
    write_private(home / "auth/state.enc", bundle.read_bytes(), repo)
    write_private(home / "fingerprint-seed", (restored["fingerprint"] + "\n").encode(), repo)
    return {"operation": "portable-import", "live_authentication_verification_required": True}


def install_service(repo: Path) -> dict:
    c, home = settings(repo)
    require(sys.platform.startswith("linux"), "Configure native durable supervision on this supported host before starting")
    require(not cdp_version(c), "Stop and export the existing research browser before replacing its service")
    py = home / "venv/bin/python"
    require(py.is_file(), "Run research-bootstrap --apply first")
    # systemd argv quoting is deliberately separate from shell quoting.
    quote_arg = lambda s: '"' + str(s).replace('\\', '\\\\').replace('"', '\\"').replace('%', '%%') + '"'
    argv = [str(py), str(repo.resolve() / "scripts/factory.py"), "--repo", str(repo.resolve()),
            "research-browser", "serve"]
    unit = ("[Unit]\nDescription=Belief Changer isolated Clearcote research browser\nAfter=network-online.target\n"
            "StartLimitIntervalSec=60\nStartLimitBurst=3\n"
            "[Service]\nType=simple\nEnvironment=" + quote_arg("BC_RESEARCH_HOME=" + str(home)) +
            "\nExecStart=" + " ".join(quote_arg(a) for a in argv) +
            "\nRestart=on-failure\nRestartSec=5\nKillMode=control-group\nTimeoutStopSec=90\n")
    target = Path.home() / ".config/systemd/user" / UNIT
    target.parent.mkdir(parents=True, exist_ok=True)
    atomic_bytes(target, unit.encode())
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=True, capture_output=True)
    return {"operation": "install", "unit": UNIT, "engine": "clearcote", "runtime": str(home)}


def start(repo: Path, allow_captcha: bool) -> dict:
    c, home = settings(repo)
    require(allow_captcha, "Explicit --allow-captcha is required for the enabled NopeCHA extension")
    require(sys.platform.startswith("linux"), "Configure this host's durable browser service before start")
    if not cdp_version(c):
        subprocess.run(["systemctl", "--user", "start", UNIT], check=True, capture_output=True)
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        result = doctor(repo)
        if result['ready']:
            return result
        time.sleep(.2)
    raise FactoryError("Clearcote research browser did not become ready; inspect its owned service")


def doctor(repo: Path) -> dict:
    c, home = settings(repo)
    version = cdp_version(c)
    receipt = home / "browser.json"
    data = read_json(receipt) if receipt.is_file() and not receipt.is_symlink() else {}
    from .research_access import extension_check
    try:
        extension_check(home/'extensions/nopecha',c)
        extension_check(home/'extensions/opencli',c,'opencli')
        intact = True
    except (FactoryError,OSError): intact = False
    ready = bool(version and data.get("engine") == "clearcote" and data.get("pid")
                 and Path('/proc', str(data["pid"])).exists()
                 and data.get('sdk_version') == c['clearcote_version']
                 and data.get('bridge_context') in bridge_profiles()
                 and data.get('bridge_context') == owned_bridge(c,home) and intact
                 and not data.get('state_export_error'))
    return {"engine": "clearcote", "ready": ready, "cdp": endpoint(c),
            "browser_version": version.get("Browser") if version else None,
            "state_present": (home / "auth/state.enc").is_file(),
            "key_present": (home / "auth/transfer.key").is_file(), "state_outside_repo": str(home)}


def ensure(repo: Path, allow_captcha: bool) -> dict:
    result = start(repo, allow_captcha)
    require(result["ready"], "Research CDP endpoint does not belong to the configured Clearcote browser")
    return result


def stop(repo: Path) -> dict:
    result = transfer(repo, "export")
    subprocess.run(["systemctl", "--user", "stop", UNIT], check=True, capture_output=True)
    return {**result, "operation": "stop", "state_saved": True}


def serve(repo: Path) -> None:
    c, home = settings(repo)
    require(not os.environ.get("CLEARCOTE_BINARY"), "Unreviewed browser binary override is not allowed")
    require(importlib.metadata.version("clearcote") == c["clearcote_version"], "Clearcote SDK differs from reviewed pin")
    from clearcote import serve as launch
    from .research_access import extension_check
    extension_check(home / "extensions/nopecha", c)
    extension_check(home / "extensions/opencli", c, 'opencli')
    seed = home / "fingerprint-seed"
    if (home/'auth/state.enc').exists():
        try: restored = json.loads(cipher(repo,home).decrypt(private_file(home/'auth/state.enc',repo,existing=True).read_bytes()))
        except Exception: raise FactoryError('Private state authentication failed before browser launch') from None
        require(isinstance(restored.get('fingerprint'),str) and restored['fingerprint'], 'Private state lacks browser identity')
        write_private(seed,(restored['fingerprint']+'\n').encode(),repo)
    if not seed.exists():
        write_private(seed, ("belief-changer-" + secrets.token_hex(16) + "\n").encode(), repo)
    private_file(seed, repo, existing=True)
    with lock(home / "browser-owner"):
        os.environ.update(environment(home))
        previous = bridge_profiles()
        server = launch(port=c["browser_port"], headless=True, quiet=True,
                        user_data_dir=str(home / "profiles/clearcote"),
                        extensions=[str(home / "extensions/nopecha"), str(home / "extensions/opencli")],
                        fingerprint=seed.read_text().strip(), disable_gpu_fingerprint=True, fingerprint_noise=False)
        restore = None
        try:
            bridge_context = bind_bridge(c, home, previous)
            if (home / "auth/state.enc").exists():
                try:
                    payload = cipher(repo, home).decrypt(private_file(home/'auth/state.enc',repo,existing=True).read_bytes())
                except Exception:
                    raise FactoryError('Private state decryption failed; research browser is not ready') from None
                argv = ['node', str(Path(__file__).with_name('research_state.cjs')), 'import-watch',
                        endpoint(c), str(home/'node/node_modules/playwright-core'), json.dumps(c['auth_domains'])]
                restore = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                restore.stdin.write(payload); restore.stdin.close(); payload = b''
                require(select.select([restore.stdout], [], [], 60)[0], 'Private state importer did not become ready')
                require(restore.stdout.readline().strip() == b'{"imported":true}', 'Private state importer failed; credentials suppressed')
            receipt={"engine": "clearcote", "pid": os.getpid(),
                     "sdk_version": c["clearcote_version"], "bridge_context": bridge_context}
            write_private(home / "browser.json", json.dumps(receipt).encode(), repo)
            signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
            while True:
                time.sleep(60)
                try:
                    transfer(repo,'export');receipt['state_export_error']=False
                except (FactoryError,OSError,subprocess.TimeoutExpired): receipt['state_export_error']=True
                write_private(home/'browser.json',json.dumps(receipt).encode(),repo)
        except KeyboardInterrupt:
            transfer(repo, "export")
        finally:
            if restore is not None:
                restore.terminate()
                try: restore.wait(timeout=10)
                except subprocess.TimeoutExpired: restore.kill(); restore.wait()
            server.close()
            (home / "browser.json").unlink(missing_ok=True)
