import socket
import sys
import threading
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import port_checker


class TestPortChecker(unittest.TestCase):
    def test_unauthorized_host(self):
        with self.assertRaises(PermissionError):
            port_checker.check_tcp_port("8.8.8.8", 53)

    def test_invalid_port_zero(self):
        with self.assertRaises(ValueError):
            port_checker.check_tcp_port("127.0.0.1", 0)

    def test_invalid_port_too_high(self):
        with self.assertRaises(ValueError):
            port_checker.check_tcp_port("127.0.0.1", 70000)

    def test_invalid_timeout(self):
        with self.assertRaises(ValueError):
            port_checker.check_tcp_port("127.0.0.1", 80, timeout=0)

    def test_closed_port_on_localhost(self):
        result = port_checker.check_tcp_port("127.0.0.1", 1, timeout=0.5)
        self.assertFalse(result["open"])
        self.assertIn("127.0.0.1", result["message"])

    def test_open_port_on_local_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]

        def accept_once():
            conn, _addr = server.accept()
            conn.close()

        thread = threading.Thread(target=accept_once, daemon=True)
        thread.start()

        try:
            result = port_checker.check_tcp_port("127.0.0.1", port, timeout=1)
            self.assertTrue(result["open"])
        finally:
            server.close()
            thread.join(timeout=1)

    def test_cli_unauthorized(self):
        code = port_checker.main(["--host", "8.8.8.8", "--port", "53"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
