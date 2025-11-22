# Menu principal

def main():
    while True:
        print("=== SISTEMA DE USUÁRIOS ===")
        print("1 - Cadastrar")
        print("2 - Login")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()

        elif opcao == "2":
            usuario = login_usuario()
            if usuario:
                menu_logado(usuario)

        elif opcao == "3":
            print("Seção encerrada...")
            break

        else:
            print("Opção inválida! Tente novamente.\n")

           
import json
import os


def carregar_usuarios():
    if not os.path.exists("usuarios.json"):
        return []
    with open("usuarios.json", "r") as arquivo:
        return json.load(arquivo)

# Salvar usuários no arquivo JSON

def salvar_usuarios(lista):
    with open("usuarios.json", "w") as arquivo:
        json.dump(lista, arquivo, indent=3)

# Cadastrar usuário

def cadastrar_usuario():
    print("\n=== CADASTRO DE USUÁRIO ===")
   
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()

    if nome == "":
        print("Erro: o nome não pode ser vazio!")
        return
    if "@" not in email or "." not in email:
        print("Erro: email inválido!")
        return
    if len(senha) < 3:
        print("Erro: a senha deve conter ao menos 3 caracteres")
        return

    usuarios = carregar_usuarios()

 # Verificação de e-mail já cadastrado
    for u in usuarios:
        if u["email"] == email:
            print("Erro: email já cadastrado!")
            return

 # Criar usuário
    novo_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha
    }

    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)

    print("Usuário cadastrado com sucesso!\n")

# Login de usuário

def login_usuario():
    print("== LOGIN ==\n")
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()

    usuarios = carregar_usuarios()

    for u in usuarios:
        if u["email"] == email and u["senha"] == senha:
            print(f"Login bem-sucedido! {u['nome']}!\n")
            return u
       
 # Retorno do usuário logado

    print("Email ou senha incorretos!\n")
    return None

def excluir_usuario(usuario):
    print("\n=== EXCLUIR USUÁRIO ===")
    confirmacao = input("Tem certeza que deseja excluir sua conta? (s/n): ").lower()

    if confirmacao != "s":
        print("Operação cancelada.")
        return False

    usuarios = carregar_usuarios()

    #  Remove o usuário
    usuarios = [u for u in usuarios if u["email"] != usuario["email"]]

    # salva o arquivo atualizado
    salvar_usuarios(usuarios)

    print("Usuário excluído com sucesso!\n")
    return True

# Menu do usuário logado

def menu_logado(usuario):
    while True:
        print("== MENU DO SISTEMA ==\n")
        print("1 - Ver meus dados")
        print("2 - Alterar nome")
        print("3 - Excluir conta")
        print("4 - Logout")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Meus dados:\n")
            print(f"Nome: {usuario['nome']}")
            print(f"Email: {usuario['email']}\n")

        elif opcao == "2":
            novo_nome = input("Novo nome: ").strip()
            if novo_nome != "":
                usuario["nome"] = novo_nome
                usuarios = carregar_usuarios()

                # Atualizar no JSON
                for u in usuarios:
                    if u["email"] == usuario["email"]:
                        u["nome"] = novo_nome

                salvar_usuarios(usuarios)
                print("Nome atualizado com sucesso!\n")
            else:
                print("O nome não pode ser vazio!")
               
        elif opcao == "3":
            if excluir_usuario(usuario):
                break

        elif opcao == "4":
            print("Logout realizado!\n")
            break

        else:
            print("Opção inválida!")