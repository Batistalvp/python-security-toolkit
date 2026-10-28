import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
EXAMPLES = ROOT / "examples"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import log_analyzer


class TestLogAnalyzer(unittest.TestCase):
    def test_sample_log(self):
        report = log_analyzer.analyze_log(str(EXAMPLES / "sample.log"))
        self.assertGreater(report["event_count"], 0)
        self.assertIn("192.168.1.10", report["unique_ips"])
        self.assertGreaterEqual(report["failed_logins"], 1)
        self.assertGreaterEqual(report["successful_logins"], 1)
        self.assertGreaterEqual(report["errors"], 1)
        self.assertTrue(report["repeated_ips"])
        self.assertTrue(report["suspicious"])

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            log_analyzer.analyze_log("log_inexistente.log")

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            log_analyzer.analyze_log(str(EXAMPLES / "sample.log"), repeat_threshold=0)

    def test_empty_log(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.log"
            path.write_text("", encoding="utf-8")
            report = log_analyzer.analyze_log(str(path))
            self.assertEqual(report["event_count"], 0)
            self.assertEqual(report["unique_ips"], [])
            self.assertEqual(report["errors"], 0)

    def test_simple_log_counts(self):
        content = (
            "INFO Successful login for user a from 10.0.0.1\n"
            "ERROR Failed login for user b from 10.0.0.2\n"
            "ERROR Failed login for user b from 10.0.0.2\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "mini.log"
            path.write_text(content, encoding="utf-8")
            report = log_analyzer.analyze_log(str(path), repeat_threshold=2)
            self.assertEqual(report["event_count"], 3)
            self.assertEqual(report["failed_logins"], 2)
            self.assertEqual(report["successful_logins"], 1)
            self.assertEqual(report["ip_counts"]["10.0.0.2"], 2)

    def test_cli_missing_file(self):
        self.assertEqual(log_analyzer.main(["--file", "nao.log"]), 1)


if __name__ == "__main__":
    unittest.main()
