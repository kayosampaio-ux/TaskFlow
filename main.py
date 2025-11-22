import os
import json
import datetime

ARQUIVO = "tarefas.json"

# ----------------------------------------------------
# CARREGAR E SALVAR TAREFAS
# ----------------------------------------------------

def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

def gerar_id():
    tarefas = carregar_tarefas()
    return 1 if not tarefas else max(t["id"] for t in tarefas) + 1

# ----------------------------------------------------
# FUNÇÕES DE TAREFAS
# ----------------------------------------------------

def criar_tarefa(titulo, descricao, responsavel, prazo):
    tarefa = {
        "id": gerar_id(),
        "titulo": titulo,
        "descricao": descricao,
        "responsavel": responsavel,
        "prazo": prazo,
        "status": "pendente"
    }

    tarefas = carregar_tarefas()
    tarefas.append(tarefa)
    salvar_tarefas(tarefas)
    print("Tarefa criada com sucesso!")

def listar_tarefas():
    tarefas = carregar_tarefas()

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    for t in tarefas:
        print("-" * 40)
        print(f"ID: {t['id']}")
        print(f"Título: {t['titulo']}")
        print(f"Responsável: {t['responsavel']}")
        print(f"Descrição: {t['descricao']}")
        print(f"Prazo: {t['prazo']}")
        print(f"Status: {t['status']}")

def validar_prazo(prazo):
    try:
        datetime.datetime.strptime(prazo, "%Y-%m-%d")
        return True
    except:
        print("Data inválida! Use o formato AAAA-MM-DD.")
        return False

def editar_tarefa(id_tarefa, novo_titulo=None, novo_prazo=None):
    tarefas = carregar_tarefas()

    for t in tarefas:
        if t["id"] == id_tarefa:

            if novo_titulo:
                t["titulo"] = novo_titulo

            if novo_prazo:
                if validar_prazo(novo_prazo):
                    t["prazo"] = novo_prazo

            salvar_tarefas(tarefas)
            print("Tarefa editada com sucesso!")
            return

    print("Tarefa não encontrada.")

def concluir_tarefa(id_tarefa):
    tarefas = carregar_tarefas()

    for t in tarefas:
        if t["id"] == id_tarefa:
            t["status"] = "concluída"
            salvar_tarefas(tarefas)
            print("Tarefa concluída!")
            return

    print("Tarefa não encontrada.")

def excluir_tarefa(id_tarefa):
    tarefas = carregar_tarefas()
    novas = [t for t in tarefas if t["id"] != id_tarefa]

    if len(novas) == len(tarefas):
        print("Tarefa não encontrada.")
        return

    salvar_tarefas(novas)
    print("Tarefa excluída!")

# ----------------------------------------------------
# RELATÓRIOS
# ----------------------------------------------------

def relatorio_concluidas(tarefas):
    texto = "TAREFAS CONCLUÍDAS\n"
    texto += "-" * 40 + "\n"
    for t in tarefas:
        if t["status"] == "concluída":
            texto += "- " + t["titulo"] + "\n"
    return texto

def relatorio_pendentes(tarefas):
    texto = "TAREFAS PENDENTES\n"
    texto += "-" * 40 + "\n"
    for t in tarefas:
        if t["status"] == "pendente":
            texto += "- " + t["titulo"] + "\n"
    return texto

def relatorio_atrasadas(tarefas):
    hoje = datetime.datetime.now().date()
    texto = "TAREFAS ATRASADAS\n"
    texto += "-" * 40 + "\n"
    for t in tarefas:
        try:
            prazo = datetime.datetime.strptime(t["prazo"], "%Y-%m-%d").date()
            if prazo < hoje and t["status"] == "pendente":
                texto += "- " + t["titulo"] + "\n"
        except:
            pass
    return texto

def exportar_txt(conteudo, nome):
    with open(nome, "w", encoding="utf-8") as arq:
        arq.write(conteudo)
    print(f"Relatório exportado como {nome}")

# ----------------------------------------------------
# MENU
# ----------------------------------------------------

def menu():
    while True:
        print("\n" + "-"*40)
        print(" SISTEMA DE TAREFAS")
        print("-"*40)
        print("1 - Criar tarefa")
        print("2 - Listar tarefas")
        print("3 - Editar tarefa")
        print("4 - Concluir tarefa")
        print("5 - Excluir tarefa")
        print("6 - Gerar relatórios")
        print("0 - Sair")
        
        opc = input("Escolha uma opção: ")

        if opc == "1":
            titulo = input("Título: ")
            descricao = input("Descrição: ")
            responsavel = input("Responsável: ")
            prazo = input("Prazo (AAAA-MM-DD): ")

            criar_tarefa(titulo, descricao, responsavel, prazo)

        elif opc == "2":
            listar_tarefas()

        elif opc == "3":
            try:
                id_tarefa = int(input("ID da tarefa: "))
            except:
                print("ID inválido.")
                continue

            novo_titulo = input("Novo título (enter mantém): ")
            novo_prazo = input("Novo prazo (AAAA-MM-DD, enter mantém): ")

            if novo_titulo == "":
                novo_titulo = None
            if novo_prazo == "":
                novo_prazo = None

            editar_tarefa(id_tarefa, novo_titulo, novo_prazo)

        elif opc == "4":
            try:
                id_tarefa = int(input("ID da tarefa: "))
                concluir_tarefa(id_tarefa)
            except:
                print("ID inválido.")

        elif opc == "5":
            try:
                id_tarefa = int(input("ID da tarefa: "))
                excluir_tarefa(id_tarefa)
            except:
                print("ID inválido.")

        elif opc == "6":
            tarefas = carregar_tarefas()
            print("\n1 - Relatório concluídas")
            print("2 - Relatório pendentes")
            print("3 - Relatório atrasadas")

            r = input("Escolha: ")

            if r == "1":
                texto = relatorio_concluidas(tarefas)
                exportar_txt(texto, "concluidas.txt")

            elif r == "2":
                texto = relatorio_pendentes(tarefas)
                exportar_txt(texto, "pendentes.txt")

            elif r == "3":
                texto = relatorio_atrasadas(tarefas)
                exportar_txt(texto, "atrasadas.txt")

            else:
                print("Opção inválida.")

        elif opc == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


menu()