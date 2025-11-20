
import os
import hashlib
import uuid
from utils.arquivos import carregar_json, salvar_json
from datetime import datetime

USUARIOS_FILE = 'usuarios.json'


class UserExistsError(Exception):
    pass


class AuthenticationError(Exception):
    pass


def _hash_senha(senha: str, salt: str = None) -> (str, str):
    if salt is None:
        salt = uuid.uuid4().hex
    h = hashlib.sha256((salt + senha).encode('utf-8')).hexdigest()
    return h, salt


def _inicializar():
    data = carregar_json(USUARIOS_FILE)
    if data is None:
        salvar_json(USUARIOS_FILE, [])
        return []
    return data


def cadastrar_usuario(username: str, nome: str, senha: str):
    usuarios = _inicializar()
    if any(u['username'] == username for u in usuarios):
        raise UserExistsError('Nome de usuário já existe')
    senha_hash, salt = _hash_senha(senha)
    novo = {
        'username': username,
        'nome': nome,
        'senha_hash': senha_hash,
        'salt': salt,
        'criado_em': datetime.utcnow().isoformat() + 'Z'
    }
    usuarios.append(novo)
    salvar_json(USUARIOS_FILE, usuarios)
    return novo


def autenticar_usuario(username: str, senha: str):
    usuarios = _inicializar()
    u = next((x for x in usuarios if x['username'] == username), None)
    if not u:
        raise AuthenticationError('Usuário não encontrado')
    senha_hash, _ = _hash_senha(senha, u['salt'])
    if senha_hash != u['senha_hash']:
        raise AuthenticationError('Senha incorreta')
    return {k: v for k, v in u.items() if k not in ('senha_hash', 'salt')}