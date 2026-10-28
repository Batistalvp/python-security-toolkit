import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import file_integrity


class TestFileIntegrity(unittest.TestCase):
    def test_same_content_not_changed(self):
        with tempfile.TemporaryDirectory() as folder:
            path_a = Path(folder) / "a.txt"
            path_b = Path(folder) / "b.txt"
            path_a.write_text("mesmo", encoding="utf-8")
            path_b.write_text("mesmo", encoding="utf-8")
            result = file_integrity.compare_files(str(path_a), str(path_b))
            self.assertFalse(result["changed"])
            self.assertEqual(result["hash_a"], result["hash_b"])

    def test_different_content_changed(self):
        with tempfile.TemporaryDirectory() as folder:
            path_a = Path(folder) / "a.txt"
            path_b = Path(folder) / "b.txt"
            path_a.write_text("antes", encoding="utf-8")
            path_b.write_text("depois", encoding="utf-8")
            result = file_integrity.compare_files(str(path_a), str(path_b))
            self.assertTrue(result["changed"])

    def test_expected_hash_ok(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "file.txt"
            content = b"hash-me"
            path.write_bytes(content)
            expected = hashlib.sha256(content).hexdigest()
            result = file_integrity.compare_with_expected(str(path), expected)
            self.assertFalse(result["changed"])

    def test_expected_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "file.txt"
            path.write_text("novo", encoding="utf-8")
            fake = "0" * 64
            result = file_integrity.compare_with_expected(str(path), fake)
            self.assertTrue(result["changed"])

    def test_invalid_expected_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "file.txt"
            path.write_text("x", encoding="utf-8")
            with self.assertRaises(ValueError):
                file_integrity.compare_with_expected(str(path), "abc")

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            file_integrity.sha256_file("nao_existe.txt")

    def test_cli_missing_file(self):
        self.assertEqual(file_integrity.main(["--file", "nao_existe.txt"]), 1)


if __name__ == "__main__":
    unittest.main()
