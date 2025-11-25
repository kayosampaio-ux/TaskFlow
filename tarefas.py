import os
import json
import datetime
ARQUIVO = "tarefas.json"

def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return []

def gerar_id():
    tarefas = carregar_tarefas()
    if not tarefas:
        return 1
    return max(t["id"] for t in tarefas) + 1

def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w") as f:
        json.dump(tarefas, f, indent=2)

def criar_tarefa(titulo, descricao, responsavel, prazo):
    tarefa = {"id": gerar_id(),'titulo': titulo,"descricao": descricao,"responsavel": responsavel,"prazo": prazo,"status": "pendente"}
    tarefas = carregar_tarefas()
    tarefas.append(tarefa)
    salvar_tarefas(tarefas)
    print("tarefa criada")

def lista_tarefas():
    tarefas = carregar_tarefas()
    if not tarefas:
        print("tarefa nao encontrada")
        return
    for t in tarefas:
        print("-" * 40)
        print("ID:", t["id"])
        print("titulo:", t["titulo"])
        print("responsavel:", t["responsavel"])
        print("descricao:", t["descricao"])
        print("prazo:", t["prazo"])
        print("status:", t["status"])

def validar_prazo(prazo):
    try:
        datetime.datetime.strptime(prazo, "%Y-%m-%d")
        return True
    except:
        print("data invalida")
        return False

def editar_tarefa(id_tarefa, novo_titulo=None, novo_prazo=None):
    tarefas = carregar_tarefas()
    for t in tarefas:
        if t["id"] == id_tarefa:
            if novo_titulo:
                t["titulo"] = novo_titulo
            if novo_prazo and validar_prazo(novo_prazo):
                t["prazo"] = novo_prazo
            salvar_tarefas(tarefas)
            print("tarefa editada")
            return
    print("tarefa não encontrada")

def concluir_tarefa(id_tarefa):
    tarefas = carregar_tarefas()

    for t in tarefas:
        if t["id"] == id_tarefa:
            t["status"] = "concluida"
            salvar_tarefas(tarefas)
            print("tarefa salva")
            return
    print("tarefa nao encontrada")

def excluir_tarefa(id_tarefa):
    tarefas = carregar_tarefas()
    nova = [t for t in tarefas if t["id"] != id_tarefa]
    if len(nova) == len(tarefas):
        print("tarefa não encontrada")
        return
    salvar_tarefas(nova)
    print("tarefa salva")
      
def menu():
    while True:
        print("\n--- MENU ---")
        print("1 - Criar")
        print("2 - Listar")
        print("3 - Editar")
        print("4 - Concluir")
        print("5 - Excluir")
        print("0 - Sair")

        opc = input("Opção: ")

        if opc == "1":
            titulo = input("Título: ")
            descricao = input("Descrição: ")
            responsavel = input("Responsável: ")
            prazo = input("Prazo (AAAA-MM-DD): ")
            criar_tarefa(titulo, descricao, responsavel, prazo)

        elif opc == "2":
            lista_tarefas()

        elif opc == "3":
            try:
                id_tarefa = int(input("ID: "))
            except:
                print("ID inválido.")
                continue

            novo_titulo = input("Novo título (enter = manter): ") or None
            novo_prazo = input("Novo prazo (AAAA-MM-DD ou enter): ") or None

            editar_tarefa(id_tarefa, novo_titulo, novo_prazo)

        elif opc == "4":
            try:
                id_tarefa = int(input("ID: "))
                concluir_tarefa(id_tarefa)
            except:
                print("ID inválido.")

        elif opc == "5":
            try:
                id_tarefa = int(input("ID: "))
                excluir_tarefa(id_tarefa)
            except:
                print("ID inválido.")

        elif opc == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

# Iniciar o menu
if __name__ == "__main__":
    menu()