"""
File Integrity — calcula SHA-256 e compara arquivos ou um hash esperado.

Integridade significa: o conteúdo continua o mesmo. Em segurança, hashes
ajudam a perceber se um arquivo foi alterado.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path


def sha256_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    if not path.is_file():
        raise IsADirectoryError(f"O caminho não é um arquivo: {file_path}")

    digest = hashlib.sha256()
    with path.open("rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def compare_files(path_a: str, path_b: str) -> dict:
    """Compara o conteúdo de dois arquivos pelo hash SHA-256."""
    hash_a = sha256_file(path_a)
    hash_b = sha256_file(path_b)
    changed = hash_a != hash_b
    return {
        "mode": "files",
        "file_a": path_a,
        "file_b": path_b,
        "hash_a": hash_a,
        "hash_b": hash_b,
        "changed": changed,
        "message": (
            "Os arquivos são diferentes. O conteúdo foi alterado."
            if changed
            else "Os arquivos são iguais. Nenhuma alteração detectada."
        ),
    }


def compare_with_expected(file_path: str, expected_hash: str) -> dict:
    """Compara o hash atual de um arquivo com um valor conhecido."""
    expected = expected_hash.strip().lower()
    if len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
        raise ValueError("O hash esperado deve ter 64 caracteres hexadecimais (SHA-256).")

    current = sha256_file(file_path)
    changed = current != expected
    return {
        "mode": "expected",
        "file": file_path,
        "current_hash": current,
        "expected_hash": expected,
        "changed": changed,
        "message": (
            "O hash atual é diferente do esperado. O arquivo mudou."
            if changed
            else "O hash atual é igual ao esperado. Integridade ok."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verifica integridade de arquivos com SHA-256."
    )
    parser.add_argument("--file", required=True, help="Arquivo principal.")
    parser.add_argument("--compare", help="Segundo arquivo para comparação.")
    parser.add_argument(
        "--expected-hash",
        help="Hash SHA-256 conhecido do arquivo (64 caracteres hex).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.compare and args.expected_hash:
        print("Erro: use --compare OU --expected-hash, não os dois.", file=sys.stderr)
        return 1

    try:
        if args.compare:
            result = compare_files(args.file, args.compare)
            print(f"Arquivo A: {result['file_a']}")
            print(f"Hash A: {result['hash_a']}")
            print(f"Arquivo B: {result['file_b']}")
            print(f"Hash B: {result['hash_b']}")
        elif args.expected_hash:
            result = compare_with_expected(args.file, args.expected_hash)
            print(f"Arquivo: {result['file']}")
            print(f"Hash atual: {result['current_hash']}")
            print(f"Hash esperado: {result['expected_hash']}")
        else:
            digest = sha256_file(args.file)
            print(f"Arquivo: {args.file}")
            print(f"SHA-256: {digest}")
            print("Passe --compare ou --expected-hash para verificar alteração.")
            print()
            print(
                "Integridade e segurança: se o hash muda, o arquivo mudou. "
                "Isso ajuda a perceber troca de arquivos, edição ou corrupção."
            )
            return 0
    except (FileNotFoundError, IsADirectoryError, OSError, ValueError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1

    print(result["message"])
    print()
    print(
        "Integridade e segurança: hashes não dizem *quem* alterou o arquivo, "
        "mas mostram se o conteúdo continua o mesmo."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
