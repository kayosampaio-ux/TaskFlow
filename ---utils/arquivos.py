
import json
import os
from typing import Any


def carregar_json(path: str) -> Any:
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Arquivo corrompido — renomear para análise futura
        os.rename(path, path + '.corrompido')
        return None


def salvar_json(path: str, data: Any):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)