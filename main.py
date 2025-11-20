
import sys
from getpass import getpass
from usuarios import cadastrar_usuario, autenticar_usuario, AuthenticationError
from tarefas import (criar_tarefa, editar_tarefa, excluir_tarefa, listar_tarefas_usuario, marcar_concluida)
from relatorios import gerar_relatorios

CURRENT_USER = None


def menu_principal():
    print("\n=== TaskFlow — Sistema de Tarefas Colaborativo ===")
    print("1. Login")
    print("2. Cadastrar usuário")
    print("3. Sair")


def menu_logado():
    print(f"\n--- Menu (usuário: {CURRENT_USER['username']}) ---")
    print("1. Gerenciar tarefas")
    print("2. Relatórios")
    print("3. Logout")


def menu_tarefas():
    print("\n--- Tarefas ---")
    print("1. Criar tarefa")
    print("2. Editar tarefa")
    print("3. Excluir tarefa")
    print("4. Listar minhas tarefas")
    print("5. Marcar como concluída")
    print("6. Voltar")


def fluxo_tarefas():
    while True:
        menu_tarefas()
        escolha = input('> ').strip()
        if escolha == '1':
            criar_tarefa(CURRENT_USER['username'])
        elif escolha == '2':
            editar_tarefa(CURRENT_USER['username'])
        elif escolha == '3':
            excluir_tarefa(CURRENT_USER['username'])
        elif escolha == '4':
            listar_tarefas_usuario(CURRENT_USER['username'])
        elif escolha == '5':
            marcar_concluida(CURRENT_USER['username'])
        elif escolha == '6':
            break
        else:
            print('Opção inválida')


def fluxo_principal():
    global CURRENT_USER
    while True:
        try:
            if not CURRENT_USER:
                menu_principal()
                opc = input('> ').strip()
                if opc == '1':
                    username = input('Usuário: ').strip()
                    senha = getpass('Senha: ')
                    try:
                        usuario = autenticar_usuario(username, senha)
                        CURRENT_USER = usuario
                        print(f'Login realizado com sucesso: {username}')
                    except AuthenticationError as e:
                        print('Erro ao autenticar:', e)
                elif opc == '2':
                    username = input('Escolha um nome de usuário: ').strip()
                    nome = input('Nome completo: ').strip()
                    senha = getpass('Senha: ')
                    senha2 = getpass('Confirme a senha: ')
                    if senha != senha2:
                        print('Senhas diferentes. Cadastro cancelado.')
                        continue
                    cadastrar_usuario(username, nome, senha)
                    print('Usuário criado com sucesso. Faça o login.')
                elif opc == '3':
                    print('Saindo...')
                    sys.exit(0)
                else:
                    print('Opção inválida')
            else:
                menu_logado()
                opc = input('> ').strip()
                if opc == '1':
                    fluxo_tarefas()
                elif opc == '2':
                    gerar_relatorios(CURRENT_USER['username'])
                elif opc == '3':
                    print(f'Logout: {CURRENT_USER["username"]}')
                    CURRENT_USER = None
                else:
                    print('Opção inválida')
        except Exception as e:
            print('[Erro global]', e)


if __name__ == '_main_':
    print('Iniciando TaskFlow...')
    fluxo_principal()