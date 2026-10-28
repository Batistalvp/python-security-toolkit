"""Caminho comum para importar as ferramentas nos testes."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
EXAMPLES = ROOT / "examples"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
