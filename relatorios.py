
from utils.arquivos import carregar_json
from datetime import datetime

TAREFAS_FILE = 'tarefas.json'


def gerar_relatorios(username: str):
    tarefas = carregar_json(TAREFAS_FILE) or []
    minhas = [t for t in tarefas if t['owner'] == username]
    totais = len(minhas)
    concluidas = len([t for t in minhas if t['concluida']])
    pendentes = totais - concluidas
    atrasadas = 0
    hoje = datetime.utcnow().date()
    for t in minhas:
        if t.get('prazo') and not t['concluida']:
            try:
                d = datetime.fromisoformat(t['prazo']).date()
            except Exception:
                try:
                    d = datetime.strptime(t['prazo'], '%Y-%m-%d').date()
                except Exception:
                    continue
            if d < hoje:
                atrasadas += 1
    print('--- Relatório de produtividade ---')
    print('Usuário:', username)
    print('Total de tarefas:', totais)
    print('Concluídas:', concluidas)
    print('Pendentes:', pendentes)
    print('Atrasadas:',atrasadas)