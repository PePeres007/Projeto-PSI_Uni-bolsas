import os
import re
import random
import time
import smtplib
from email.message import EmailMessage

# ----------------------------
# Funções Utilitárias
# ----------------------------
def enviar_email(destinatario, codigo):
    email_remetente = "pedroperesb25@gmail.com"         # <-- Meu email
    senha_app = "mfqjzbdknwelrern"                 # <-- Minha senha de app

    msg = EmailMessage()
    msg["Subject"] = "Seu código de verificação"
    msg["From"] = email_remetente
    msg["To"] = destinatario
    msg.set_content(f"Olá! Seu código de verificação é: {codigo}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_remetente, senha_app)
            smtp.send_message(msg)
        print("📧 Código de verificação enviado para o seu email!")
    except Exception as e:
        print("❌ Erro ao enviar email:", e)

def limpar_terminal():
    os.system('cls')

# ----------------------------
# Validações
# ----------------------------

def validar_nome():
    while True:
        nome = input("Digite seu nome completo: ").strip().title()
        if re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome):
            return nome
        else:
            print("Nome inválido! Use apenas letras e espaços (sem números ou símbolos).")

def validar_email():
    while True:
        email = input("Digite seu email: (Ex: usuario@ufrpe.br) ").strip().lower()
        erros = []
        if "@" not in email:
            erros.append("faltando '@'")
        if not re.search(r"\.(br)$", email):
            erros.append("faltando (.br) ou domínio inválido (.com, .org, .br)")
        if not re.search(r"@(ufrpe)\.br", email):
            erros.append("faltando (ufrpe) ou provedor de domínio inválido (gmail, hotmail, outlook)")

        if not erros:
            return email
        print(f"Email inválido: {', '.join(erros)}")


def validar_senha(email):
    while True:
        senha = input("Digite sua senha (Somente letras e números, 8 caracteres, ex: Senha123): ").strip()

        if not senha.isalnum():
            print("Senha inválida. Use apenas letras e números (sem símbolos ou espaços).")
            continue

        if len(senha) == 8 and re.search(r"[A-Z]", senha) and re.search(r"[0-9]", senha):
            confirmar_senha = input("Confirme sua senha: ").strip()
            if confirmar_senha == senha:
                codigo = random.randint(100000, 999999)
                enviar_email(email, codigo)  # ⬅️ envia o código por email
                while True:
                    codigo_digitado = input("Digite o código de verificação enviado por email: ").strip()
                    if codigo_digitado == str(codigo):
                        print("Código correto! Cadastro confirmado.")
                        return senha
                    else:
                        print("Código incorreto. Tente novamente.")
            else:
                print("As senhas não coincidem. Tente novamente.")
        else:
            print("Senha inválida. Deve conter 8 caracteres, uma letra maiúscula e um número.")


# ----------------------------
# Cadastro de Usuário
# ----------------------------
def cadastrar_usuario():
    print("=== Cadastro de Usuário ===\n")
    nome = validar_nome()
    email = validar_email()
    senha = validar_senha(email)


    with open("usuarios.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome};{email};{senha}\n")

    limpar_terminal()
    print("✅ Cadastro realizado com sucesso!")
    print(f"Nome: {nome}")
    print(f"Email: {email}")
    print("Sua senha foi salva com segurança!")

    print("\nLimpando a tela em:")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    limpar_terminal()

# ----------------------------
# Listagem de Usuários
# ----------------------------
def listar_usuarios():
    try:
        with open("usuarios.txt", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        if not linhas:
            print("Nenhum usuário cadastrado ainda.")
            return

        print("=== Lista de Usuários Cadastrados ===\n")
        for i, linha in enumerate(linhas, 1):
            nome, email, senha = linha.strip().split(";")
            print(f"{i}. Nome: {nome} | Email: {email}")
    except FileNotFoundError:
        print("Arquivo de usuários não encontrado.")

    print("\nLimpando a tela em:")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)


# ----------------------------
# Exclusão de Usuário
# ----------------------------
def excluir_usuario():
    try:
        with open("usuarios.txt", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        if not linhas:
            print("Nenhum usuário cadastrado.")
            return

        email_excluir = input("Digite o email do usuário que deseja excluir: ").strip().lower()
        nova_lista = []
        encontrado = False

        for linha in linhas:
            nome, email, senha = linha.strip().split(";")
            if email != email_excluir:
                nova_lista.append(linha)
            else:
                encontrado = True

        if encontrado:
            with open("usuarios.txt", "w", encoding="utf-8") as arquivo:
                arquivo.writelines(nova_lista)
            print(f"Usuário com email '{email_excluir}' foi excluído com sucesso.")
        else:
            print("Usuário não encontrado.")
    except FileNotFoundError:
        print("Arquivo de usuários não encontrado.")

    print("\nLimpando a tela em:")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    limpar_terminal()

# ----------------------------
# Menu Principal
# ----------------------------
def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Cadastrar novo usuário")
        print("2 - Listar usuários")
        print("3 - Excluir usuário")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            limpar_terminal()
            cadastrar_usuario()
        elif opcao == "2":
            limpar_terminal()
            listar_usuarios()
        elif opcao == "3":
            limpar_terminal()
            excluir_usuario()
        elif opcao == "4":
            print("Encerrando o programa. Até mais!")
            limpar_terminal()
            break
        else:
            print("Opção inválida. Tente novamente.")
            limpar_terminal()

# ----------------------------
# Execução
# ----------------------------
if __name__ == "__main__":
    menu()
