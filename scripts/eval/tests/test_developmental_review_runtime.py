"""RF-13 exact isolated-runtime filesystem inventory regressions."""
import os
import shutil
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import developmental_review as DEV  # noqa: E402
import developmental_review_runtime as RUNTIME  # noqa: E402
from developmental_review_fixture import DevelopmentalFixture  # noqa: E402


class DevelopmentalRuntimeTests(DevelopmentalFixture, unittest.TestCase):
    def test_every_runtime_entry_has_one_exact_flat_identity(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        task = DEV.prepare(self.ready("runtime-inventory"))
        root = RUNTIME.validate(task)

        def mutate(action):
            root.chmod(0o700)
            action()
            root.chmod(0o555)

        def reject(label, install, remove):
            with self.subTest(entry=label):
                mutate(install)
                try:
                    with self.assertRaises(RUNTIME.RuntimeError):
                        RUNTIME.validate(task)
                finally:
                    mutate(remove)
                self.assertEqual(root, RUNTIME.validate(task))

        extra = root / "undeclared.json"
        def add_extra():
            extra.write_text("{}", encoding="utf-8")
            extra.chmod(0o444)
        reject("unexpected file", add_extra, extra.unlink)

        empty = root / "empty"
        reject("empty directory", lambda: empty.mkdir(mode=0o555), empty.rmdir)

        nested, leaf = root / "nested", root / "nested/leaf"
        def add_nested():
            nested.mkdir(mode=0o700)
            leaf.mkdir(mode=0o555)
            nested.chmod(0o555)
        def remove_nested():
            nested.chmod(0o700)
            shutil.rmtree(nested)
        reject("nested directories", add_nested, remove_nested)

        alias = root / "task-alias"
        reject("file alias", lambda: alias.symlink_to(RUNTIME.task_path(
            task["task_sha256"])), alias.unlink)

        directory_alias = root / "directory-alias"
        reject("directory alias", lambda: directory_alias.symlink_to(root,
            target_is_directory=True), directory_alias.unlink)

        linked = root / "task-hardlink"
        reject("hard link", lambda: os.link(RUNTIME.task_path(
            task["task_sha256"]), linked), linked.unlink)

        for target, mode, canonical in ((root, 0o755, 0o555),
                (RUNTIME.task_path(task["task_sha256"]), 0o644, 0o444),
                (RUNTIME.schema_path(task["task_sha256"]), 0o400, 0o444)):
            with self.subTest(target=target.name, mode=oct(mode)):
                target.chmod(mode)
                try:
                    with self.assertRaises(RUNTIME.RuntimeError):
                        RUNTIME.validate(task)
                finally:
                    target.chmod(canonical)
                self.assertEqual(root, RUNTIME.validate(task))


if __name__ == "__main__":
    unittest.main()
