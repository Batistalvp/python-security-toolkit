import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import ip_validator


class TestIpValidator(unittest.TestCase):
    def test_private_ip(self):
        info = ip_validator.classify_ipv4("192.168.0.10")
        self.assertTrue(info["valid"])
        self.assertTrue(info["is_private"])
        self.assertFalse(info["is_public"])
        self.assertIn("privado", info["category"])

    def test_another_private_range(self):
        info = ip_validator.classify_ipv4("10.0.0.1")
        self.assertTrue(info["is_private"])

    def test_loopback(self):
        info = ip_validator.classify_ipv4("127.0.0.1")
        self.assertTrue(info["is_loopback"])
        self.assertFalse(info["is_public"])

    def test_public_documentation_address(self):
        # 8.8.8.8 é um DNS público conhecido; usamos só para classificação.
        info = ip_validator.classify_ipv4("8.8.8.8")
        self.assertTrue(info["is_public"])
        self.assertFalse(info["is_private"])

    def test_invalid_text(self):
        with self.assertRaises(ValueError):
            ip_validator.classify_ipv4("nao-e-ip")

    def test_invalid_octet(self):
        with self.assertRaises(ValueError):
            ip_validator.classify_ipv4("999.1.1.1")

    def test_ipv6_rejected(self):
        with self.assertRaises(ValueError):
            ip_validator.classify_ipv4("::1")

    def test_cli_valid(self):
        self.assertEqual(ip_validator.main(["192.168.1.1"]), 0)

    def test_cli_invalid(self):
        self.assertEqual(ip_validator.main(["abc"]), 1)


if __name__ == "__main__":
    unittest.main()
