import os
import re
import random
import time
import smtplib
from email.message import EmailMessage

# ----------------------------
# Variáveis Globais
# ----------------------------
ARQUIVO_USUARIOS = "usuarios.txt"
EMAIL_REMETENTE = "pedroperesb25@gmail.com"
SENHA_APP = "mfqjzbdknwelrern"
EMAIL_ADM = "ppbenicio10@gmail.com"
NOME_ADM = "Pedro Peres Benicio"

# ----------------------------
# Utilitários
# ----------------------------
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def enviar_email(destinatario, codigo, info):
    msg = EmailMessage()
    msg["Subject"] = "UniBolsas - Código de segurança"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario
    msg.set_content(f"{info} {codigo}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(msg)
        print(" Código de verificação enviado para o seu email!")
    except Exception as e:
        print(" Erro ao enviar email:", e)

# ----------------------------
# Validações
# ----------------------------
def validar_nome():
    while True:
        nome = input("Digite seu nome completo: ").strip().title()
        if re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome):
            return nome
        else:
            print("Nome inválido! Use apenas letras e espaços.")

def validar_email():
    while True:
        email = input("Digite seu email (Ex: usuario@ufrpe.br): ").strip().lower()
        erros = []
        if "@" not in email:
            erros.append("faltando '@'")
        if not re.search(r".br$", email):
            erros.append("faltando domínio .br")
        if not re.search(r"@(ufrpe).br$", email):
            erros.append("provedor inválido (ex: ufrpe.br)")

        if not erros:
            return email
        print(f"Email inválido: {', '.join(erros)}")

def validar_senha(email):
    while True:
        senha = input("Crie sua nova senha (8 caracteres, apenas letras e números, ex: Senha123): ").strip()

        if not senha.isalnum():
            print("Senha inválida. Use apenas letras e números (sem símbolos).")
            continue

        if len(senha) == 8 and re.search(r"[A-Z]", senha) and re.search(r"[0-9]", senha):
            confirmar_senha = input("Confirme sua senha: ").strip()
            if confirmar_senha == senha:
                codigo = random.randint(100000, 999999)
                mensagem = ("Código para validação de indentidade e confirmação de senha: ")
                enviar_email(email, codigo, mensagem)
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
# Gerenciamento de Usuários
# ----------------------------
def email_ja_cadastrado(email):
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                _, e, _ = linha.strip().split(";")
                if e == email:
                    return True
    except FileNotFoundError:
        pass
    return False

def cadastrar_usuario():
    print("=== Cadastro de Usuário ===\n")
    nome = validar_nome()
    email = validar_email()

    if email_ja_cadastrado(email):
        print("Este email já está cadastrado. Redirecionando para o menu de login...")
        time.sleep(2)
        return None

    senha = validar_senha(email)
    with open(ARQUIVO_USUARIOS, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome};{email};{senha}\n")

    print("✅ Cadastro realizado com sucesso!")
    print("Limpando a tela...")
    time.sleep(2)
    limpar_terminal()
    return email

def login():
    print("=== Login ===")
    email = input("Email: ").strip().lower()
    if email == EMAIL_ADM:
        codigo = random.randint(100000, 999999)
        mensagem = ("òtimo dia administrador, aqui está seu codigo de acesso: ")
        enviar_email(email, codigo, mensagem)
        codigo_digitado = input("Digite o código enviado ao email do administrador: ")
        if str(codigo_digitado) == str(codigo):
            print("✅ Login de administrador bem-sucedido!")
            return (NOME_ADM, EMAIL_ADM)
        else:
            print("❌ Código incorreto.")
            return None

    senha = input("Senha: ").strip()
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                nome, e, s = linha.strip().split(";")
                if e == email and s == senha:
                    print("✅ Login bem-sucedido!")
                    return (nome, email)
    except FileNotFoundError:
        pass

    print("❌ Email ou senha inválidos.")
    return None

def listar_usuarios():
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        if not linhas:
            print("Nenhum usuário cadastrado ainda.")
            return

        print("\n=== Lista de Usuários Cadastrados ===\n")
        for i, linha in enumerate(linhas, 1):
            nome, email, _ = linha.strip().split(";")
            print(f"{i}. Nome: {nome} | Email: {email}")
    except FileNotFoundError:
        print("Arquivo de usuários não encontrado.")

    print("\nVoltando ao menu...")
    time.sleep(2)

def excluir_usuario():
    email_excluir = input("Digite o email do usuário que deseja excluir: ").strip().lower()
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        nova_lista = [linha for linha in linhas if linha.strip().split(";")[1] != email_excluir]

        if len(nova_lista) == len(linhas):
            print("Usuário não encontrado.")
        else:
            with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
                arquivo.writelines(nova_lista)
            print("Usuário excluído com sucesso!")
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    time.sleep(2)

def alterar_dados_usuario(email_usuario):
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        nova_lista = []
        for linha in linhas:
            nome, email, senha = linha.strip().split(";")
            if email == email_usuario:
                print("O que deseja alterar?")
                print("1 - Nome")
                print("2 - Senha")
                escolha = input("Escolha uma opção: ")
                if escolha == "1":
                    nome = validar_nome()
                elif escolha == "2":
                    senha_antiga = input("Digite sua senha antiga: ")
                    if senha_antiga == senha:
                        senha = validar_senha(email)
                    else:
                        print("Senha invalida. Retornando para alteração de dados")
                        alterar_dados_usuario(email_usuario)
                else:
                    print("Opção inválida.")
                nova_lista.append(f"{nome};{email};{senha}\n")
            else:
                nova_lista.append(linha)

        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(nova_lista)
        print("Dados alterados com sucesso!")
    except Exception as e:
        print("Erro ao alterar dados:", e)


def redefinir_senha():
    print("\n=== Redefinir Senha ===")
    email = input("Digite seu email: ").strip().lower()

    if not email_ja_cadastrado(email):
        print("❌ Email não encontrado.")
        return

    # Envia código de verificação
    codigo = random.randint(100000, 999999)
    mensagem = "Código para redefinição de senha:"
    enviar_email(email, codigo, mensagem)

    for tentativa in range(3):
        codigo_digitado = input("Digite o código enviado ao seu email: ").strip()
        if codigo_digitado == str(codigo):
            print("✅ Código correto.")
            nova_senha = validar_senha(email)

            # Atualiza a senha no arquivo
            try:
                with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
                    linhas = arquivo.readlines()

                with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
                    for linha in linhas:
                        nome, e, senha_antiga = linha.strip().split(";")
                        if e == email:
                            arquivo.write(f"{nome};{email};{nova_senha}\n")
                        else:
                            arquivo.write(linha)
                print("✅ Senha redefinida com sucesso!")
                return
            except Exception as e:
                print("Erro ao redefinir senha:", e)
                return
        else:
            print("❌ Código incorreto. Tente novamente.")

    print("Número máximo de tentativas excedido.")

# ----------------------------
# Menus
# ----------------------------
def menu_adm():
    while True:
        print("\n=== MENU ADMINISTRADOR ===")
        print("1 - Gerenciar Sistema")
        print("2 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_gerenciar_sistema()
        elif opcao == "2":
            break
        else:
            print("Opção inválida.")


def menu_usuario(nome, email):
    while True:
        print(f"\nBem-vindo, {nome}!")
        print("1 - Configurações")
        print("2 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = menu_configuracoes(nome, email)  # ← atualiza o nome
        elif opcao == "2":
            break
        else:
            print("Opção inválida.")

# ----------------------------
#Menus de Crud
#-----------------------------
def menu_configuracoes(nome, email):
    while True:
        print("\n=== CONFIGURAÇÕES ===")
        print("1 - Ver minhas informações")
        print("2 - Alterar meus dados")
        print("3 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print(f"\nNome: {nome}")
            print(f"Email: {email}")
        elif opcao == "2":
            alterar_dados_usuario(email)
            # Atualiza o nome após alteração
            try:
                with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
                    for linha in arquivo:
                        nome_lido, email_lido, _ = linha.strip().split(";")
                        if email_lido == email:
                            nome = nome_lido
                            break
            except FileNotFoundError:
                print("Erro ao atualizar nome em memória.")
        elif opcao == "3":
            return nome  # ← retorna o nome atualizado
        else:
            print("Opção inválida.")

def menu_gerenciar_sistema():
    while True:
        print("\n=== GERENCIAR SISTEMA ===")
        print("1 - Cadastrar novo usuário")
        print("2 - Listar usuários")
        print("3 - Excluir usuário")
        print("4 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            excluir_usuario()
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")


# ----------------------------
# Execução Principal
# ----------------------------
def menu_login_cadastro():
    limpar_terminal()
    while True:
        print("1 - Login")
        print("2 - Cadastrar-se")
        print("3 - Redefinir senha")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            resultado = login()
            if resultado:
                nome, email = resultado
                if email == EMAIL_ADM:
                    menu_adm()
                else:
                    menu_usuario(nome, email)
        elif opcao == "2":
            email_cadastrado = cadastrar_usuario()
            if email_cadastrado:
                continue
        elif opcao == "3":
            redefinir_senha()
        elif opcao == "4":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_login_cadastro()
