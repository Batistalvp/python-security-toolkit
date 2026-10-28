"""
Cloud Config Checker — analisa um JSON fictício de configuração de nuvem.

Isto é uma simulação educacional. Não conecta em AWS, Azure ou Google Cloud
e não substitui uma auditoria real.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


RISKY_PORTS = {22, 3389, 3306, 5432, 27017, 6379}


def load_config(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo JSON não encontrado: {file_path}")
    if not path.is_file():
        raise IsADirectoryError(f"O caminho não é um arquivo: {file_path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"JSON inválido: {error}") from error

    if not isinstance(data, dict):
        raise ValueError("O JSON deve ser um objeto (dicionário), não uma lista.")
    return data


def analyze_config(config: dict) -> list[dict]:
    """
    Percorre o dicionário e gera uma lista de achados.
    Cada achado tem campo, status (ok/atencao) e motivo.
    """
    findings = []

    storage_public = config.get("storage_public")
    if storage_public is True:
        findings.append(
            {
                "field": "storage_public",
                "status": "atencao",
                "reason": "Armazenamento público pode expor arquivos para qualquer pessoa na internet.",
            }
        )
    elif storage_public is False:
        findings.append(
            {
                "field": "storage_public",
                "status": "ok",
                "reason": "O armazenamento não está marcado como público.",
            }
        )
    else:
        findings.append(
            {
                "field": "storage_public",
                "status": "atencao",
                "reason": "Campo ausente ou inválido. Em Cloud, deixe explícito se o bucket é privado.",
            }
        )

    encryption = config.get("encryption_enabled")
    if encryption is True:
        findings.append(
            {
                "field": "encryption_enabled",
                "status": "ok",
                "reason": "Criptografia habilitada ajuda a proteger dados em repouso.",
            }
        )
    else:
        findings.append(
            {
                "field": "encryption_enabled",
                "status": "atencao",
                "reason": "Sem criptografia, um vazamento de disco ou backup fica mais fácil de ler.",
            }
        )

    authentication = config.get("authentication_enabled")
    if authentication is True:
        findings.append(
            {
                "field": "authentication_enabled",
                "status": "ok",
                "reason": "Autenticação habilitada exige identidade para acessar o recurso.",
            }
        )
    else:
        findings.append(
            {
                "field": "authentication_enabled",
                "status": "atencao",
                "reason": "Sem autenticação, o serviço pode aceitar acesso anônimo.",
            }
        )

    mfa = config.get("mfa_enabled")
    if mfa is True:
        findings.append(
            {
                "field": "mfa_enabled",
                "status": "ok",
                "reason": "MFA adiciona um segundo fator além da senha.",
            }
        )
    elif "mfa_enabled" in config:
        findings.append(
            {
                "field": "mfa_enabled",
                "status": "atencao",
                "reason": "MFA desabilitada deixa contas mais frágeis se a senha vazar.",
            }
        )

    logging = config.get("logging_enabled")
    if logging is True:
        findings.append(
            {
                "field": "logging_enabled",
                "status": "ok",
                "reason": "Logs ajudam a investigar acessos e erros.",
            }
        )
    elif "logging_enabled" in config:
        findings.append(
            {
                "field": "logging_enabled",
                "status": "atencao",
                "reason": "Sem logs, fica difícil perceber acessos indevidos.",
            }
        )

    backup = config.get("backup_enabled")
    if backup is True:
        findings.append(
            {
                "field": "backup_enabled",
                "status": "ok",
                "reason": "Backup habilitado ajuda na recuperação após falha.",
            }
        )
    elif "backup_enabled" in config:
        findings.append(
            {
                "field": "backup_enabled",
                "status": "atencao",
                "reason": "Sem backup, um apagamento acidental pode ser irreversível.",
            }
        )

    open_ports = config.get("open_ports", [])
    if not isinstance(open_ports, list):
        findings.append(
            {
                "field": "open_ports",
                "status": "atencao",
                "reason": "open_ports deveria ser uma lista de números.",
            }
        )
    else:
        risky = [port for port in open_ports if port in RISKY_PORTS]
        if 0 in open_ports:
            findings.append(
                {
                    "field": "open_ports",
                    "status": "atencao",
                    "reason": "Porta 0 não é um serviço válido neste contexto.",
                }
            )
        if risky:
            findings.append(
                {
                    "field": "open_ports",
                    "status": "atencao",
                    "reason": (
                        f"Portas sensíveis abertas: {risky}. "
                        "Exponha administração (SSH/RDP) e bancos só para redes confiáveis."
                    ),
                }
            )
        elif open_ports:
            findings.append(
                {
                    "field": "open_ports",
                    "status": "ok",
                    "reason": f"Portas listadas: {open_ports}. Revise se todas são realmente necessárias.",
                }
            )

    networks = config.get("allowed_networks", [])
    if isinstance(networks, list) and "0.0.0.0/0" in networks:
        findings.append(
            {
                "field": "allowed_networks",
                "status": "atencao",
                "reason": "0.0.0.0/0 significa qualquer IP da internet. Restrinja a redes conhecidas.",
            }
        )

    return findings


def summarize(findings: list[dict]) -> dict:
    attention = [item for item in findings if item["status"] == "atencao"]
    ok_items = [item for item in findings if item["status"] == "ok"]
    return {
        "findings": findings,
        "attention_count": len(attention),
        "ok_count": len(ok_items),
        "attention": attention,
        "ok": ok_items,
    }


def format_report(file_path: str, summary: dict) -> str:
    lines = [
        "=== Cloud Config Checker (simulação educacional) ===",
        "Isto NÃO é uma auditoria real e NÃO acessa contas de nuvem.",
        f"Arquivo: {file_path}",
        f"Itens ok: {summary['ok_count']}",
        f"Itens que precisam de atenção: {summary['attention_count']}",
        "",
        "Detalhes:",
    ]
    for item in summary["findings"]:
        label = "ATENÇÃO" if item["status"] == "atencao" else "OK"
        lines.append(f"  [{label}] {item['field']}: {item['reason']}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analisa um JSON fictício de configuração de Cloud."
    )
    parser.add_argument(
        "--file",
        default="examples/sample_cloud_config.json",
        help="Caminho do JSON. Padrão: examples/sample_cloud_config.json",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_config(args.file)
        summary = summarize(analyze_config(config))
    except (FileNotFoundError, IsADirectoryError, OSError, ValueError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1

    print(format_report(args.file, summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
