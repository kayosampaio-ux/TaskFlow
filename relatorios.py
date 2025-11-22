from tarefas import ARQUIVO


def relatorio_concluidas(tarefas):
    texto = "TAREFAS CONCLUÍDAS\n"
    texto += "----------------------\n"

    for t in tarefas:
        if t["status"] == "concluida":
            texto += "- " + t["titulo"] + "\n"

    return texto


def relatorio_pendentes(tarefas):
    texto = "TAREFAS PENDENTES\n"
    texto += "----------------------\n"

    for t in tarefas:
        if t["status"] == "pendente":
            texto += "- " + t["titulo"] + "\n"

    return texto


def relatorio_atrasadas(tarefas):
    texto = "TAREFAS ATRASADAS\n"
    texto += "----------------------\n"

    for t in tarefas:
        if t["status"] == "atrasada":
            texto += "- " + t["titulo"] + "\n"

    return texto


def exportar_txt(texto, nome):
    arquivo = open(nome, "w", encoding="utf-8")
    arquivo.write(texto)
    arquivo.close()
    