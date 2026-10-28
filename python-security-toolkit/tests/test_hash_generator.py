import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import hash_generator


class TestHashGenerator(unittest.TestCase):
    def test_same_text_same_hash(self):
        first = hash_generator.generate_text_hash("laboratorio")
        second = hash_generator.generate_text_hash("laboratorio")
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

    def test_different_text_different_hash(self):
        first = hash_generator.generate_text_hash("abc")
        second = hash_generator.generate_text_hash("abd")
        self.assertNotEqual(first, second)

    def test_matches_hashlib(self):
        text = "ADS-2026"
        expected = hashlib.sha256(text.encode("utf-8")).hexdigest()
        self.assertEqual(hash_generator.generate_text_hash(text), expected)

    def test_file_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.txt"
            path.write_text("conteudo de teste", encoding="utf-8")
            digest = hash_generator.generate_file_hash(str(path))
            expected = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, expected)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            hash_generator.generate_file_hash("arquivo_que_nao_existe.txt")

    def test_directory_is_rejected(self):
        with self.assertRaises(IsADirectoryError):
            hash_generator.generate_file_hash(str(TOOLS))

    def test_cli_text(self):
        code = hash_generator.main(["--text", "ola"])
        self.assertEqual(code, 0)

    def test_cli_missing_file(self):
        code = hash_generator.main(["--file", "nao_existe.bin"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
