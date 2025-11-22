
import json

def salvar_json(dados, caminho_arquivo):

    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)