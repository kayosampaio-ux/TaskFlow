
from utils.arquivos import carregar_json, salvar_json
from datetime import datetime
import uuid

TAREFAS_FILE = 'tarefas.json'


def _inicializar():
    data = carregar_json(TAREFAS_FILE)
    if data is None:
        salvar_json(TAREFAS_FILE, [])
        return []
    return data


def criar_tarefa(owner_username: str):
    tarefas = _inicializar()
    titulo = input('Título: ').strip()
    descricao = input('Descrição (opcional): ').strip()
    prazo = input('Data de vencimento (YYYY-MM-DD) ou vazio: ').strip()
    tarefa = {
        'id': uuid.uuid4().hex,
        'owner': owner_username,
        'titulo': titulo,
        'descricao': descricao,
        'criado_em': datetime.utcnow().isoformat() + 'Z',
        'prazo': prazo if prazo else None,
        'concluida': False,
        'concluida_em': None
    }
    tarefas.append(tarefa)
    salvar_json(TAREFAS_FILE, tarefas)
    print('Tarefa criada:', tarefa['id'])


def listar_tarefas_usuario(owner_username: str):
    tarefas = _inicializar()
    minhas = [t for t in tarefas if t['owner'] == owner_username]
    if not minhas:
        print('Nenhuma tarefa encontrada.')
        return
    for t in minhas:
        status = 'Concluída' if t['concluida'] else 'Pendente'
        print('---')
        print('ID:', t['id'])
        print('Título:', t['titulo'])
        print('Descrição:', t['descricao'])
        print('Prazo:', t['prazo'])
        print('Status:', status)
        if t['concluida']:
            print('Concluída em:', t['concluida_em'])


def achar_tarefa_por_id(tarefas, id, owner_username):
    return next((t for t in tarefas if t['id'] == id_ and t['owner'] == owner_username), None)


def editar_tarefa(owner_username: str):
    tarefas = _inicializar()
    id_ = input('ID da tarefa para editar: ').strip()
    t = achar_tarefa_por_id(tarefas, id, owner_username)
    if not t:
        print('Tarefa não encontrada ou você não tem permissão')
        return
    novo_titulo = input(f'Título [{t["titulo"]}]: ').strip() or t['titulo']
    nova_desc = input(f'Descrição [{t["descricao"]}]: ').strip() or t['descricao']
    novo_prazo = input(f'Prazo [{t.get("prazo")}]: ').strip() or t.get('prazo')
    t['titulo'] = novo_titulo
    t['descricao'] = nova_desc
    t['prazo'] = novo_prazo
    salvar_json(TAREFAS_FILE, tarefas)
    print('Tarefa atualizada')


def excluir_tarefa(owner_username: str):
    tarefas = _inicializar()
    id_ = input('ID da tarefa para excluir: ').strip()
    t = achar_tarefa_por_id(tarefas, id, owner_username)
    if not t:
        print('Tarefa não encontrada ou você não tem permissão')
        return
    tarefas.remove(t)
    salvar_json(TAREFAS_FILE, tarefas)
    print('Tarefa removida')


def marcar_concluida(owner_username: str):
    tarefas = _inicializar()
    id_ = input('ID da tarefa para marcar como concluída: ').strip()
    t = achar_tarefa_por_id(tarefas, id, owner_username)
    if not t:
        print('Tarefa não encontrada ou você não tem permissão')
        return
    if t['concluida']:
        print('Tarefa já está marcada como concluída')
        return
    t['concluida'] = True
    t['concluida_em'] = datetime.utcnow().isoformat() + 'Z'
    salvar_json(TAREFAS_FILE, tarefas)
    print('Tarefa marcada como concluída')