from usuarios import main as menu_usuarios
from tarefas import menu as menu_tarefas


def main():
    while True:
        print("\n===== SISTEMA GERAL =====")
        print("1 - Sistema de Usuários")
        print("2 - Sistema de Tarefas")
        print("0 - Sair")

        opc = input("Escolha uma opção: ")

        if opc == "1":
            # abre o menu do usuarios.py
            menu_usuarios()

        elif opc == "2":
            # abre o menu das tarefas
            menu_tarefas()

        elif opc == "0":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida!")

# Executa
main()