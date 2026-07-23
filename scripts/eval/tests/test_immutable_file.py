"""Cross-platform interrupted write-once recovery regressions."""
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import immutable_file as IMMUTABLE  # noqa: E402


class ImmutableFileTests(unittest.TestCase):
    def test_identical_retry_restores_canonical_read_only_state(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "evidence.json"
            data = b'{"durable":true}\n'
            with mock.patch.object(Path, "chmod", side_effect=OSError("interrupted")):
                with self.assertRaisesRegex(IMMUTABLE.ImmutableFileError, "interrupted"):
                    IMMUTABLE.write_once(path, data, Path.read_bytes, "evidence")
            info = os.lstat(path)
            if os.name == "nt":
                self.assertFalse(getattr(info, "st_file_attributes", 0)
                                 & getattr(stat, "FILE_ATTRIBUTE_READONLY", 0))
            else:
                self.assertTrue(stat.S_IMODE(info.st_mode) & stat.S_IWUSR)

            IMMUTABLE.write_once(path, data, Path.read_bytes, "evidence")
            info = os.lstat(path)
            if os.name == "nt":
                self.assertTrue(getattr(info, "st_file_attributes", 0)
                                & getattr(stat, "FILE_ATTRIBUTE_READONLY", 0))
            else:
                self.assertEqual(0o444, stat.S_IMODE(info.st_mode))
            with self.assertRaisesRegex(IMMUTABLE.ImmutableFileError, "differs"):
                IMMUTABLE.write_once(path, b"different\n", Path.read_bytes, "evidence")
            path.chmod(0o644)


if __name__ == "__main__":
    unittest.main()
