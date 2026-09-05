#!/usr/bin/env python3
"""Spawn Cursor composer-2.5 ask-mode judges for one replicate."""
from __future__ import annotations

import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO = Path(os.environ.get("BC_REPO", "/home/kab/Belief-changer"))
SLUG = os.environ.get("SLUG", "quit-sugar")
REF_DIR = Path(os.environ.get("REF_DIR", str(REPO / "calibration/reference/gsbs")))
JUDGES = REPO / "loop/judges"
AGENT = Path.home() / ".local/bin/agent"
LANES = ("belief-mechanic", "voice-emotion", "reader-journey")
COMPARISON = "chapter-comparison"
# Founder 2026-09-04: 10-wide → 40 jobs in 4 waves on this 15 GiB MemTotal box.
JUDGE_PARALLEL = int(os.environ.get("JUDGE_PARALLEL", "10"))


def parse_alignment(text: str) -> dict[int, int]:
    out: dict[int, int] = {}
    for line in text.splitlines():
        m = re.match(r"\|\s*0?(\d+)\s*\|\s*.*?\|\s*Ch\s*0?(\d+)\s*", line)
        if m:
            out[int(m.group(1))] = int(m.group(2))
    if not out:
        raise SystemExit("no alignment rows parsed")
    return out


def extract_cards(plan: str) -> dict[int, str]:
    parts = re.split(r"\n(?=(?:#{1,3}\s+|\*\*)(?:CH-|C-)\d{1,2}\s+—)", plan)
    cards: dict[int, str] = {}
    for p in parts:
        m = re.match(r"(?:#{1,3}\s+|\*\*)(?:CH-|C-)(\d{1,2})\s+—", p)
        if m:
            cards[int(m.group(1))] = p.strip()
    return cards


def parse_inventory_table(plan: str, header: str) -> dict[str, str]:
    out: dict[str, str] = {}
    in_table = False
    for line in plan.splitlines():
        if header.lower() in line.lower():
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 2 or cols[0] in ("ID", "---") or set(cols[0]) <= {"-"}:
            continue
        iid = cols[0].strip("* ")
        wording = cols[1]
        if re.match(r"^(M|FT|I|T)-[A-Z0-9]+$", iid):
            out[iid] = wording
    if not out:
        current = None
        for line in plan.splitlines():
            hm = re.match(r"\*\*((?:M|FT|I|T)-[A-Z0-9]+) —", line)
            if hm:
                current = hm.group(1)
                continue
            if current:
                wm = re.match(r"- Wording:\s*(.+)", line)
                if wm:
                    out[current] = wm.group(1).strip()
                    current = None
    return out


def field(card: str, name: str) -> str:
    needle = name.lower()
    for line in card.splitlines():
        stripped = line.lstrip("*-# \t").lower()
        if stripped.startswith(needle) and ":" in line:
            return line.split(":", 1)[1].strip()
    for part in card.split(" | "):
        cleaned = part.lstrip("* ").lower()
        if cleaned.startswith(needle) and ":" in part:
            return part.split(":", 1)[1].strip()
    return "NONE"


def ids_in(blob: str) -> list[str]:
    return re.findall(r"\b(?:M-[A-Z]|M-\d+|FT-\d+|I-\d+|T-[A-Z])\b", blob)


def chapter_context(n: int, n_total: int, card: str, mantras: dict[str, str], instructions: dict[str, str], tokens: dict[str, str]) -> str:
    title = card.splitlines()[0].replace("**", "").strip()
    job = field(card, "primary job")
    entering = field(card, "entering belief")
    leaving = field(card, "leaving belief")
    if entering == "NONE" and leaving == "NONE":
        belief_now = field(card, "belief now")
        if belief_now != "NONE":
            if "→" in belief_now:
                left, right = belief_now.split("→", 1)
                entering = left.replace("entry believes", "").replace("was", "", 1).strip(" \"'")
                leaving = right.replace("makes true", "").strip(" \"'")
            else:
                entering = belief_now
                leaving = belief_now
    arc = field(card, "arc")
    curve = field(card, "curve")
    if curve == "NONE":
        curve = field(card, "arc position")
    cont = field(card, "continuity")
    instr_blob = field(card, "instruction")
    if instr_blob == "NONE":
        instr_blob = field(card, "new instruction")
    if instr_blob == "NONE":
        instr_blob = field(card, "new instructions")
    mantra_blob = field(card, "mantra")
    if mantra_blob == "NONE":
        mantra_blob = field(card, "mantras/tokens")
    if mantra_blob == "NONE":
        mantra_blob = field(card, "mantras")
    instr_lines = []
    if instr_blob.lower() in ("none", "none required", ""):
        instr_lines.append("NONE")
    else:
        for iid in ids_in(instr_blob) or []:
            instr_lines.append(f"{iid}: {instructions.get(iid, '(unresolved)')}")
        if "mid-recap" in instr_blob.lower() or "recap" in instr_blob.lower():
            instr_lines.append(f"(card note: {instr_blob})")
        if not instr_lines:
            instr_lines.append(instr_blob)
    mantra_lines = []
    debut = set(ids_in(re.sub(r"echo.*", "", mantra_blob, flags=re.I)))
    for iid in ids_in(mantra_blob):
        kind = "debut" if iid in debut and "debut" in mantra_blob.lower() else "echo"
        if iid.startswith("M"):
            wording = mantras.get(iid, "(unresolved)")
        else:
            wording = tokens.get(iid, mantras.get(iid, "(unresolved)"))
        if f"debut {iid}" in mantra_blob.replace("debut:", "debut ") or mantra_blob.find("debut " + iid) >= 0:
            kind = "debut"
        elif "echo " + iid in mantra_blob or f"echo {iid}" in mantra_blob:
            kind = "echo"
        elif iid in debut and "debut" in mantra_blob.lower() and "echo " + iid not in mantra_blob:
            kind = "debut"
        mantra_lines.append(f"{iid} ({kind}): {wording}")
    if not mantra_lines:
        mantra_lines.append(mantra_blob or "NONE")
    return f"""CHAPTER CONTEXT
Chapter {n} of {n_total} — {title}
Primary job: {job}
Entering belief: {entering}
Leaving belief: {leaving}
Arc and curve position: arc: {arc}; curve: {curve}
Continuity: {cont}
Assigned compliance:
- Instruction: {"; ".join(instr_lines) if instr_lines else "NONE"}
- Mantras: {"; ".join(mantra_lines) if mantra_lines else "NONE"}
"""


def parse_moves(text: str) -> dict[int, str]:
    out: dict[int, str] = {}
    current: int | None = None
    buf: list[str] = []
    for line in text.splitlines():
        hm = re.match(r"^## (?:GSBS|EASYWAY|REF) (\d+)", line)
        if hm:
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current = int(hm.group(1))
            buf = [line]
            continue
        if current is not None:
            if line.startswith("## ") and not re.match(r"^## (?:GSBS|EASYWAY|REF) ", line):
                out[current] = "\n".join(buf).strip()
                current = None
                buf = []
            else:
                buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    if not out:
        raise SystemExit("no reference-moves parsed")
    return out


def comparison_prompt(n: int, our: Path, real: Path, ctx: str, moves: str) -> str:
    return f"""You are a book factory judge, fresh and reference-sighted. This is a single isolated judge call. There is no host task except this call.

Read {JUDGES / "_shared.md"} first, then read and follow the rubric at {JUDGES / "chapter-comparison.md"} exactly. The shared file is law; the rubric adds class tests.

OUR CHAPTER path: {our}
THE REAL CHAPTER path: {real}

BELIEF MOVES (closed list — use only these):

{moves}

Use this CHAPTER CONTEXT exactly (copied from the accepted plan card — do not improvise):

{ctx}

Read our chapter and the real chapter from those paths. Judge that pair against the rubric and shared law.

Return your verdict exactly as the rubric demands, including CLUSTER CENSUS with every closed class listed (zeros included). Start your report with PASS. Quote the evidence for each MOVE line.

Never reference scores, history, or prior judgments. Do not write any files. Do not search the rest of the repository beyond the named paths. Your entire reply IS the judge report.
"""


def lane_prompt(lane: str, n: int, our: Path, real: Path, ctx: str, prev: Path | None) -> str:
    prev_line = f"PREVIOUS CHAPTER path: {prev}\n" if prev else "PREVIOUS CHAPTER: none (chapter 1)\n"
    return f"""You are a book factory judge, fresh and reference-sighted. This is a single isolated judge call. There is no host task except this call.

Read {JUDGES / "_shared.md"} first, then read and follow the rubric at {JUDGES / f"{lane}.md"} exactly. The shared file is law; the rubric adds class tests.

OUR CHAPTER path: {our}
THE REAL CHAPTER path: {real}
{prev_line}
Use this CHAPTER CONTEXT exactly (copied from the accepted plan card — do not improvise):

{ctx}

Read our chapter and the real chapter from those paths. Judge that pair against the rubric and shared law.

Return your verdict exactly as the rubric demands, including CLUSTER CENSUS with every closed class listed (zeros included). Start your report with PASS or FAIL as the rubric requires. Quote the evidence for each verdict line.

Never reference scores, history, or prior judgments. Do not write any files. Do not search the rest of the repository beyond the named paths. Your entire reply IS the judge report.
"""


def book_arc_prompt(our_chapters: list[Path], sheets: Path, alignment: Path) -> str:
    lines = "\n".join(f"- Ch{i}: {p}" for i, p in enumerate(our_chapters, 1))
    return f"""You are a book factory judge, fresh and reference-sighted. This is a single isolated book-arc judge call. There is no host task except this call.

Read {JUDGES / "_shared.md"} first, then read and follow {JUDGES / "book-arc.md"} exactly.

OUR BOOK — every chapter in order (writer output):
{lines}

THE PLAN'S BOOK-LEVEL SHEETS: {sheets}
REFERENCE SKELETON: {alignment}

Return your verdict exactly as the rubric demands, including CLUSTER CENSUS with every closed class listed (zeros included). Start with PASS or FAIL. Hydra lock: same job done by a new scene ID is re-argument noted, never a new class, never a book FAIL by itself. PASS even if re-argument is 12, as long as every blocking count is 0.

Never reference scores, history, or prior judgments. Do not write any files. Your entire reply IS the judge report.
"""


def run_agent(prompt: str, out: Path, tag: str) -> bool:
    out.parent.mkdir(parents=True, exist_ok=True)
    (out.parent / "prompt.md").write_text(prompt)
    partial = out.with_suffix(out.suffix + ".partial")
    cmd = [
        str(AGENT),
        "--trust",
        "--model", "composer-2.5",
        "--mode", "ask",
        "-p",
        "--output-format", "text",
        prompt,
    ]
    for attempt in (1, 2):
        t0 = time.time()
        r = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True)
        text = r.stdout
        if r.returncode != 0 and not text.strip():
            text = (r.stderr or "") + f"\n\n(agent exit {r.returncode})"
        (out.parent / "metadata.json").write_text(
            '{"model":"composer-2.5","harness":"cursor-agent-cli",'
            f'"spawn":"agent --trust --model composer-2.5 --mode ask -p","latency_s":{round(time.time()-t0,3)},'
            f'"exit":{r.returncode},"attempt":{attempt}}}\n'
        )
        if r.returncode == 0 or text.lstrip().startswith(("PASS", "FAIL")):
            partial.write_text(text)
            partial.rename(out)
            print(f"OK {out.relative_to(REPO)} {round(time.time()-t0,1)}s", flush=True)
            return True
        print(f"FAIL {tag} attempt {attempt} exit {r.returncode}", flush=True)
    return False


def main() -> None:
    it = os.environ["ITER"]
    rep = os.environ["REPLICATE"]
    only = os.environ.get("ONLY")
    slug = os.environ.get("SLUG", SLUG)
    ref_dir = Path(os.environ.get("REF_DIR", str(REF_DIR)))
    alignment = Path(os.environ.get("ALIGNMENT", str(REPO / f"loop/reference-alignment-{slug}.md")))
    if not alignment.exists():
        alignment = REPO / "loop/reference-alignment.md"
    moves_path = Path(os.environ.get("MOVES", str(REPO / f"loop/reference-moves-{slug}.md")))
    if not moves_path.exists():
        moves_path = REPO / "loop/reference-moves.md"
    root = REPO / "loop/iterations" / it / slug / f"replicate-{rep}"
    if not (root / "traces").exists():
        legacy = REPO / "loop/iterations" / it / f"replicate-{rep}"
        if (legacy / "traces").exists():
            root = legacy
    traces = root / "traces"
    judgments = root / "judgments"
    judgments.mkdir(parents=True, exist_ok=True)
    plan = (traces / "plan.md").read_text() if (traces / "plan.md").exists() else (REPO / "production-books" / slug / "master-plan.md").read_text()
    cards = extract_cards(plan)
    n_total = max(cards)
    align = parse_alignment(alignment.read_text())
    moves_by_ref = parse_moves(moves_path.read_text())
    mantras = parse_inventory_table(plan, "**Mantras (repetition law")
    if not mantras:
        mantras = parse_inventory_table(plan, "Mantras (repetition law")
    if not mantras:
        mantras = parse_inventory_table(plan, "**Mantras —")
    if not mantras:
        mantras = parse_inventory_table(plan, "MANTRA AND FROZEN-TOKEN")
    tokens = parse_inventory_table(plan, "**Frozen tokens")
    if not tokens:
        tokens = parse_inventory_table(plan, "Frozen tokens")
    instructions = parse_inventory_table(plan, "Instruction spine")
    if not instructions:
        instructions = parse_inventory_table(plan, "**Instruction spine")
    sheets = judgments / "plan-sheets.md"
    m = re.search(r"(## 3\. MANTRA AND FROZEN-TOKEN SHEET\n.*?)(?=\n## 7\. )", plan, re.S | re.I)
    sheets.write_text((m.group(1) if m else plan[plan.find("## 3."):plan.find("## 7.")]) + "\n")

    jobs: list[tuple[str, Path, str]] = []
    our_paths = []
    for n in sorted(cards):
        our = traces / f"chapter-{n:02d}" / "response.md"
        our_paths.append(our)
        ref_n = align.get(n)
        if not ref_n:
            raise SystemExit(f"no reference alignment for {slug} chapter {n}")
        real = ref_dir / f"chapter-{ref_n:02d}.md"
        ctx = chapter_context(n, n_total, cards[n], mantras, instructions, tokens)
        prev = traces / f"chapter-{n-1:02d}" / "response.md" if n > 1 else None
        for lane in LANES:
            tag = f"{lane}-ch{n:02d}"
            out = judgments / tag / "response.md"
            prompt = lane_prompt(lane, n, our, real, ctx, prev)
            jobs.append((tag, out, prompt))
        move_block = moves_by_ref.get(ref_n or -1)
        if not move_block:
            raise SystemExit(f"no reference-moves for {slug} ref {ref_n} (our ch {n})")
        ctag = f"{COMPARISON}-ch{n:02d}"
        jobs.append((ctag, judgments / ctag / "response.md", comparison_prompt(n, our, real, ctx, move_block)))
    arc_out = judgments / "book-arc" / "response.md"
    jobs.append(("book-arc", arc_out, book_arc_prompt(our_paths, sheets, alignment)))

    if only:
        jobs = [j for j in jobs if j[0] == only or j[0].startswith(only)]
        if not jobs:
            raise SystemExit(f"no jobs match ONLY={only}")

    filtered = []
    for tag, out, prompt in jobs:
        if tag != "book-arc":
            n = int(re.search(r"ch(\d+)", tag).group(1))
            if not (traces / f"chapter-{n:02d}" / "response.md").exists():
                print(f"defer {tag} (chapter not written)", flush=True)
                continue
        else:
            missing = [p for p in our_paths if not p.exists()]
            if missing:
                print(f"defer book-arc missing {len(missing)} chapters", flush=True)
                continue
        if out.exists():
            print(f"skip {tag}", flush=True)
            continue
        filtered.append((tag, out, prompt))

    if not filtered:
        print("PANEL DONE", flush=True)
        return
    with ThreadPoolExecutor(max_workers=min(JUDGE_PARALLEL, len(filtered))) as pool:
        futs = {pool.submit(run_agent, prompt, out, tag): tag for tag, out, prompt in filtered}
        for tag, _, _ in filtered:
            print(f"spawn {tag}", flush=True)
        bad = [futs[fut] for fut in as_completed(futs) if not fut.result()]
    print("PANEL DONE", flush=True)
    if bad:
        raise SystemExit(f"{len(bad)} judge(s) missing after retry: {bad} — re-run to retry; existing reports are skipped")


if __name__ == "__main__":
    main()
