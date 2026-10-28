"""
Log Analyzer — lê um arquivo de log fictício e resume eventos.

Análise de logs é usada em monitoramento e segurança para perceber
falhas, acessos e padrões suspeitos. Os dados de exemplo são fictícios.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
FAILED_LOGIN_PATTERN = re.compile(r"Failed login", re.IGNORECASE)
SUCCESS_LOGIN_PATTERN = re.compile(r"Successful login", re.IGNORECASE)
ERROR_PATTERN = re.compile(r"\bERROR\b", re.IGNORECASE)


def read_log_lines(file_path: str) -> list[str]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de log não encontrado: {file_path}")
    if not path.is_file():
        raise IsADirectoryError(f"O caminho não é um arquivo: {file_path}")

    lines = []
    with path.open("r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if line:
                lines.append(line)
    return lines


def analyze_log(file_path: str, repeat_threshold: int = 3) -> dict:
    """
    Analisa o log e devolve um dicionário com contagens e alertas.
    """
    if repeat_threshold < 1:
        raise ValueError("O limiar de repetição deve ser pelo menos 1.")

    lines = read_log_lines(file_path)
    ips: list[str] = []
    failed_logins = 0
    successful_logins = 0
    errors = 0

    for line in lines:
        ips.extend(IP_PATTERN.findall(line))
        if FAILED_LOGIN_PATTERN.search(line):
            failed_logins += 1
        if SUCCESS_LOGIN_PATTERN.search(line):
            successful_logins += 1
        if ERROR_PATTERN.search(line):
            errors += 1

    ip_counts = Counter(ips)
    repeated_ips = {
        ip: count for ip, count in ip_counts.items() if count >= repeat_threshold
    }

    suspicious: list[str] = []
    if failed_logins >= repeat_threshold:
        suspicious.append(
            f"{failed_logins} tentativas de login falhas. "
            "Vale investigar se alguém tentou várias senhas."
        )
    for ip, count in repeated_ips.items():
        suspicious.append(
            f"O IP {ip} aparece {count} vezes. "
            "Repetição alta pode indicar automação ou tentativas repetidas."
        )

    failed_ips = Counter()
    for line in lines:
        if FAILED_LOGIN_PATTERN.search(line):
            found = IP_PATTERN.findall(line)
            failed_ips.update(found)
    for ip, count in failed_ips.items():
        if count >= repeat_threshold:
            suspicious.append(
                f"Várias falhas de login a partir de {ip} ({count} vezes)."
            )

    unique_suspicious = []
    for item in suspicious:
        if item not in unique_suspicious:
            unique_suspicious.append(item)

    return {
        "file": file_path,
        "event_count": len(lines),
        "unique_ips": sorted(ip_counts.keys()),
        "ip_counts": dict(ip_counts),
        "successful_logins": successful_logins,
        "failed_logins": failed_logins,
        "errors": errors,
        "repeated_ips": repeated_ips,
        "suspicious": unique_suspicious,
    }


def format_report(report: dict) -> str:
    lines = [
        f"Arquivo: {report['file']}",
        f"Eventos: {report['event_count']}",
        f"Logins com sucesso: {report['successful_logins']}",
        f"Tentativas de login falhas: {report['failed_logins']}",
        f"Linhas de erro: {report['errors']}",
        "",
        "IPs encontrados:",
    ]
    if report["unique_ips"]:
        for ip in report["unique_ips"]:
            lines.append(f"  - {ip} ({report['ip_counts'][ip]} ocorrência(s))")
    else:
        lines.append("  (nenhum IP encontrado)")

    lines.append("")
    lines.append("IPs com múltiplas ocorrências:")
    if report["repeated_ips"]:
        for ip, count in report["repeated_ips"].items():
            lines.append(f"  - {ip}: {count}")
    else:
        lines.append("  (nenhum acima do limiar)")

    lines.append("")
    lines.append("Possíveis padrões suspeitos:")
    if report["suspicious"]:
        for item in report["suspicious"]:
            lines.append(f"  - {item}")
    else:
        lines.append("  (nenhum padrão destacado)")

    lines.append("")
    lines.append(
        "Por que analisar logs? Em segurança e monitoramento, os logs "
        "mostram o que aconteceu no sistema. Contar erros e falhas de "
        "login ajuda a perceber problemas cedo, ainda em um laboratório."
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analisa um arquivo de log fictício e resume eventos."
    )
    parser.add_argument(
        "--file",
        default="examples/sample.log",
        help="Caminho do log. Padrão: examples/sample.log",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        help="Quantas vezes um IP precisa aparecer para ser destacado.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        report = analyze_log(args.file, args.threshold)
    except (FileNotFoundError, IsADirectoryError, OSError, ValueError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1

    print(format_report(report))
    print()
    print("Os dados deste exemplo são fictícios. Não use logs reais de terceiros.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
