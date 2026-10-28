"""
IP Validator — valida um endereço IPv4 e classifica como privado ou público.

Usa a biblioteca padrão ipaddress. Não realiza varredura de rede.
"""

from __future__ import annotations

import argparse
import ipaddress
import sys


def classify_ipv4(address: str) -> dict:
    """
    Analisa um IPv4 e devolve um dicionário com informações básicas.

    Levanta ValueError se o valor não for um IPv4 válido.
    """
    text = address.strip()
    try:
        ip = ipaddress.IPv4Address(text)
    except ipaddress.AddressValueError as error:
        raise ValueError(f"IPv4 inválido: {address}") from error

    info = {
        "address": str(ip),
        "valid": True,
        "version": 4,
        "is_private": ip.is_private,
        "is_public": not ip.is_private and not ip.is_loopback and not ip.is_reserved and not ip.is_multicast,
        "is_loopback": ip.is_loopback,
        "is_reserved": ip.is_reserved,
        "is_multicast": ip.is_multicast,
        "category": "",
    }

    if ip.is_loopback:
        info["category"] = "loopback (esta máquina)"
    elif ip.is_private:
        info["category"] = "privado (rede interna)"
    elif ip.is_multicast:
        info["category"] = "multicast"
    elif ip.is_reserved:
        info["category"] = "reservado"
    else:
        info["category"] = "público (internet)"

    return info


def format_report(info: dict) -> str:
    lines = [
        f"Endereço: {info['address']}",
        f"Válido: sim",
        f"Versão: IPv{info['version']}",
        f"Categoria: {info['category']}",
        f"Privado: {'sim' if info['is_private'] else 'não'}",
        f"Público: {'sim' if info['is_public'] else 'não'}",
        f"Loopback: {'sim' if info['is_loopback'] else 'não'}",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Valida um IPv4 e informa se é privado ou público."
    )
    parser.add_argument("ip", help="Endereço IPv4, por exemplo 192.168.0.10")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        info = classify_ipv4(args.ip)
    except ValueError as error:
        print(f"Erro: {error}", file=sys.stderr)
        print("Exemplo válido: 192.168.0.10", file=sys.stderr)
        return 1

    print(format_report(info))
    print()
    print("Conceito: um IP privado fica em redes internas (casa, laboratório, empresa).")
    print("Um IP público é roteável na internet. Use apenas redes autorizadas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
