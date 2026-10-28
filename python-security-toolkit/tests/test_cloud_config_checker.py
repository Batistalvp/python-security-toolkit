import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
EXAMPLES = ROOT / "examples"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import cloud_config_checker


class TestCloudConfigChecker(unittest.TestCase):
    def test_sample_config_has_attention_items(self):
        config = cloud_config_checker.load_config(str(EXAMPLES / "sample_cloud_config.json"))
        findings = cloud_config_checker.analyze_config(config)
        summary = cloud_config_checker.summarize(findings)
        self.assertGreater(summary["attention_count"], 0)
        fields = [item["field"] for item in summary["attention"]]
        self.assertIn("storage_public", fields)
        self.assertIn("authentication_enabled", fields)

    def test_secure_config(self):
        config = {
            "storage_public": False,
            "encryption_enabled": True,
            "authentication_enabled": True,
            "mfa_enabled": True,
            "open_ports": [443],
            "allowed_networks": ["10.0.0.0/8"],
            "logging_enabled": True,
            "backup_enabled": True,
        }
        summary = cloud_config_checker.summarize(cloud_config_checker.analyze_config(config))
        self.assertEqual(summary["attention_count"], 0)
        self.assertGreater(summary["ok_count"], 0)

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "broken.json"
            path.write_text("{nao json", encoding="utf-8")
            with self.assertRaises(ValueError):
                cloud_config_checker.load_config(str(path))

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            cloud_config_checker.load_config("config_inexistente.json")

    def test_json_list_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "list.json"
            path.write_text(json.dumps([1, 2, 3]), encoding="utf-8")
            with self.assertRaises(ValueError):
                cloud_config_checker.load_config(str(path))

    def test_cli_sample(self):
        code = cloud_config_checker.main(
            ["--file", str(EXAMPLES / "sample_cloud_config.json")]
        )
        self.assertEqual(code, 0)

    def test_cli_missing(self):
        self.assertEqual(cloud_config_checker.main(["--file", "nao.json"]), 1)


if __name__ == "__main__":
    unittest.main()
