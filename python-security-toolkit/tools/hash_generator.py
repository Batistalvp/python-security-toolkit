"""
Hash Generator — gera SHA-256 de texto ou arquivo.

Uso educacional: hashes servem para verificar integridade, não para
recuperar o conteúdo original nem para quebrar senhas.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path


HASH_EXPLANATION = """
O que é um hash?
Um hash é um valor de tamanho fixo calculado a partir de um dado.
O SHA-256 sempre gera 64 caracteres hexadecimais (256 bits).

Propriedades úteis em segurança:
- Determinístico: o mesmo arquivo gera o mesmo hash.
- Sensível a mudanças: alterar um byte muda o hash.
- Unidirecional: não dá para "desfazer" o hash e obter o texto original.

Como isso ajuda na integridade?
Se você guarda o hash de um arquivo confiável e, depois, gera o hash
de novo, hashes iguais indicam que o conteúdo não mudou. Hashes
diferentes indicam alteração (corrupção, edição ou troca do arquivo).

Este programa NÃO quebra hashes e NÃO recupera senhas.
"""


def generate_text_hash(text: str) -> str:
    """Retorna o SHA-256 hexadecimal de um texto."""
    data = text.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def generate_file_hash(file_path: str) -> str:
    """Retorna o SHA-256 hexadecimal de um arquivo, lendo em partes."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    if not path.is_file():
        raise IsADirectoryError(f"O caminho não é um arquivo: {file_path}")

    sha256 = hashlib.sha256()
    with path.open("rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Gera SHA-256 de um texto ou arquivo (uso educacional)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Texto que será convertido em hash.")
    group.add_argument("--file", help="Caminho de um arquivo local.")
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Mostra uma explicação sobre hashes e integridade.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.text is not None:
            digest = generate_text_hash(args.text)
            source = "texto"
        else:
            digest = generate_file_hash(args.file)
            source = f"arquivo {args.file}"
    except (FileNotFoundError, IsADirectoryError, OSError, TypeError, ValueError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1

    print(f"Algoritmo: SHA-256")
    print(f"Origem: {source}")
    print(f"Hash: {digest}")

    if args.explain:
        print(HASH_EXPLANATION)
    else:
        print("Dica: use --explain para revisar o conceito de hash e integridade.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
