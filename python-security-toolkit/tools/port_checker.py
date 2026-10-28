"""
Port Checker — testa UMA conexão TCP em um host autorizado.

Ferramenta educacional e defensiva:
- não faz varredura de portas;
- não faz força bruta;
- não explora serviços.
Use somente em localhost ou em sistemas que você administra.
"""

from __future__ import annotations

import argparse
import socket
import sys


DEFAULT_TIMEOUT_SECONDS = 3.0
ALLOWED_HOSTS = {"127.0.0.1", "localhost", "::1"}


def is_authorized_host(host: str) -> bool:
    """Permite apenas loopback, para evitar testes em redes de terceiros."""
    return host.strip().lower() in ALLOWED_HOSTS


def check_tcp_port(host: str, port: int, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> dict:
    """
    Tenta conectar em host:porta via TCP e devolve o resultado.

    Não tenta várias portas. Não ignora o timeout.
    """
    if not is_authorized_host(host):
        raise PermissionError(
            "Host não autorizado. Use 127.0.0.1 ou localhost "
            "(somente ambientes próprios)."
        )

    if not isinstance(port, int) or port < 1 or port > 65535:
        raise ValueError("A porta deve ser um número inteiro entre 1 e 65535.")

    if timeout <= 0:
        raise ValueError("O timeout deve ser maior que zero.")

    result = {
        "host": host,
        "port": port,
        "timeout": timeout,
        "open": False,
        "message": "",
    }

    try:
        with socket.create_connection((host, port), timeout=timeout):
            result["open"] = True
            result["message"] = f"A porta {port} aceitou a conexão TCP em {host}."
    except socket.timeout:
        result["message"] = (
            f"Tempo esgotado ao conectar em {host}:{port}. "
            "A porta pode estar fechada ou filtrada."
        )
    except ConnectionRefusedError:
        result["message"] = (
            f"Conexão recusada em {host}:{port}. "
            "Normalmente a porta está fechada."
        )
    except OSError as error:
        result["message"] = f"Falha de rede ao conectar em {host}:{port}: {error}"

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Testa uma única porta TCP em localhost (uso educacional)."
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host autorizado. Padrão: 127.0.0.1",
    )
    parser.add_argument(
        "--port",
        type=int,
        required=True,
        help="Uma porta TCP (1-65535).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Timeout em segundos. Padrão: 3",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    print("Aviso: use esta ferramenta somente em sistemas próprios ou autorizados.")
    print("Este programa testa UMA porta. Não é um scanner.")
    print()

    try:
        result = check_tcp_port(args.host, args.port, args.timeout)
    except (PermissionError, ValueError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1

    status = "aberta" if result["open"] else "não disponível"
    print(f"Host: {result['host']}")
    print(f"Porta: {result['port']}")
    print(f"Timeout: {result['timeout']}s")
    print(f"Resultado: {status}")
    print(result["message"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
