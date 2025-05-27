import os
import re
import random
import time
import smtplib
from email.message import EmailMessage


# Variáveis Globais
# --------------------------------
ARQUIVO_USUARIOS = "usuarios.txt"
ARQUIVO_BOLSAS = "bolsas.txt"
EMAIL_REMETENTE = "pedroperesb25@gmail.com"
SENHA_APP = "mfqjzbdknwelrern"
EMAIL_ADM = "ppbenicio10@gmail.com"
NOME_ADM = "Pedro Peres Benicio"

# ----------------------------
# funcionalidades extras
# ---------------------------
def limpar_terminal():
    """Limpa a tela com o comando cls se o sistema oeracional for windows,
    senão limpa com o comando clear"""
    os.system('cls' if os.name == 'nt' else 'clear')

def enviar_email(destinatario, codigo, info):
    """
       Envia um email com um código de verificação para o destinatário especificado.

       Parâmetros:
       destinatario (str): Endereço de email do destinatário.
       codigo (str): Código aleatório de verificação que será enviado.
       info (str): Mensagem explicativa sobre para que é o código.

       Funciona usando o servidor SMTP do Gmail com conexão SSL.
       Requer as constantes EMAIL_REMETENTE e SENHA_APP que são variaváveis globais.

       retorno:
       Em caso de sucesso, exibe uma mensagem de confirmação no terminal.
       Em caso de erro, exibe uma mensagem de erro com o motivo.
       """
    msg = EmailMessage() # define o objeto msg com a clase EmailMessage
    msg["Subject"] = "UniBolsas - Código de segurança"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario
    msg.set_content(f"{info} {codigo}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp: #Essa é uma classe da biblioteca smtplib que permite enviar e-mails usando o protocolo SMTP com SSL direto na conexão.
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(msg)
        print(" Código de verificação enviado para o seu email!")
    except Exception as e:
        print(" Erro ao enviar email:", e)

def email_ja_cadastrado(email):
    """
        Verifica se o e-mail já está cadastrado em alguma linha da lista no arquivo 'usuarios.txt'

        Parâmetro:
        email (str): email ou inserido pelo usuário durante o cadastro ou do usuário logado no momento.

        retorno:
        Em caso de sucesso, caso o e-mail ja esteja cadastrado, retorna True.
        Caso contrario, False

        Exceções:
        FileNotFoundError:  Caso o arquivo 'usuarios.txt' não exista, a função trata a exceção internamente com pass e retorna False.
    """
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                _, e, _ = linha.strip().split(";")
                if e == email:
                    return True
    except FileNotFoundError:
        pass
    return False

def listar_titulos_bolsas():
    """
        Lê o arquivo de bolsas e exibe uma lista numerada apenas com os títulos das bolsas cadastradas.

        Retorno:
        Uma lista com todas as linhas do arquivo 'bolsas.txt', onde cada linha representa uma bolsa cadastrada.
        Caso o arquivo não exista ou esteja vazio, retorna uma lista vazia.

        Exceções:
        FileNotFoundError: Exibe uma mensagem de erro caso o arquivo de bolsas não seja encontrado.

        Observação:
        O título da bolsa é considerado como o segundo campo (índice 1) em cada linha, separado por ponto e vírgula.
    """
    try:
        with open(ARQUIVO_BOLSAS, "r", encoding="utf-8") as arquivo:
            bolsas = arquivo.readlines()
            if not bolsas:
                print("Nenhuma bolsa cadastrada.")
                return []

            print("\n=== Títulos das Bolsas Cadastradas ===")
            for i, linha in enumerate(bolsas):
                dados = linha.strip().split(";")
                titulo = dados[1]
                print(f"{i + 1}. {titulo}")
            return bolsas
    except FileNotFoundError:
        print("Arquivo de bolsas não encontrado.")
        return []

def validar_texto(caracteres, vazio = False):
    """
       Recebe os dados que serão validaos por utra função e valida se contém apenas letras, espaços, vírgulas ou pontos.

       Parâmetros:
        caracteres (str): Texto que será recebido pra ser validado.
        vazio (bool, opcional): Define se a entrada pode ser vazia, é definida como False por padrão, porem se for alterado
        para true, permite a entrada vazia ("").

       Retorno:
        str ou None: Retorna o texto inserido, já com espaços removidos das extremidades, se for validado.
        Retorna None se `vazio` for True e a entrada for vazia.

       Validação:
        A entrada só é considerada válida se contiver apenas:
        - Letras (maiúsculas e minúsculas);
        - Caracteres acentuados (á, é, ç);
        - Espaços;
        - Vírgulas ou pontos.

       Observação:
        Mostra mensagem de erro caso a entrada seja inválida, solicitando nova tentativa.
    """
    while True:
        texto = input(f"{caracteres}: ").strip()
        if vazio and texto == "":
            return None
        if re.fullmatch(r"[A-Za-zÀ-ÿ\s,.]+", texto):
            return texto
        else:
            print("Entrada inválida. Use apenas letras, espaços, virgulas e pontos.")

def validar_numero(numero, vazio = False):
    """
       Recebe os dados que serão validaos de outra função e valida se contém apenas número(real ou inteiro).

       Parâmetros:
        numero (str): Valor que será recebido pra ser validado.
        vazio (bool, opcional): Define se a entrada pode ser vazia, é definida como False por padrão, porem se for alterado
        para true, permite a entrada vazia ("").

       Retorno:
        str ou None: Retorna o valor inserido, já com espaços removidos das extremidades, se for validado.
        Retorna None se `vazio` for True e a entrada for vazia.

       Validação:
        A entrada só é considerada válida se contiver apenas:
        - Letras (maiúsculas e minúsculas);
        - Caracteres acentuados (á, é, ç);
        - Espaços;
        - Vírgulas ou pontos.

       Observação:
        Mostra mensagem de erro caso a entrada seja inválida, solicitando nova tentativa.
    """
    while True:
        valor = input(f"{numero}: ").strip()
        if vazio and valor == "":
            return None
        if re.fullmatch(r"\d+(\.\d{2})?", valor):
            return valor
        else:
            print("Entrada inválida. Digite apenas números inteiros.")

# ----------------------------
# Validações
# ----------------------------
def validar_nome():
    """
        Solicita ao usuário que digite seu nome completo para a validação.

         Validação:
        A entrada só é considerada válida se contiver apenas:
        - Letras (maiúsculas e minúsculas);
        - Caracteres acentuados (á, é, ç);
        - Espaços.

        Retorno:
            Nome completo (validado e no formato correto).
    """

    while True:
        nome = input("Digite seu nome completo: ").strip().title()
        if re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome):
            return nome
        else:
            print("Nome inválido! Use apenas letras e espaços.")

def validar_email():
    """
    Solicita ao usuário que digite seu e-mail institucional para a validação.

    validação :
     - Contém o caractere '@';
     - Termina com '.br';
     - Está no formato institucional da UFRPE (ex: usuario@ufrpe.br).

    Retorno:
        e-mail validado e formatado em letras minúsculas, com espaços removidos das extremidades.

    Observação:
        Caso o e-mail seja inválido, exibe uma mensagem de erro específica indicando o(s) problema(s), ques estão na lista 'erros',
        e solicita nova tentativa até que o e-mail seja válido.
    """

    while True:
        email = input("Digite seu email (Ex: usuario@ufrpe.br): ").strip().lower()
        erros = []
        if "@" not in email:
            erros.append("faltando '@'")
        if not re.search(r".br$", email):
            erros.append("faltando domínio .br")
        if not re.search(r"@ufrpe.br$", email):
            erros.append("provedor inválido (ex: ufrpe.br)")

        if not erros:
            return email
        print(f"Email inválido: {', '.join(erros)}")

def validar_senha(email):
    """
    Solicita ao usuário a criação de uma senha segura, valida os critérios e confirma a identidade por e-mail.

    A senha deve atender aos seguintes critérios:
        - Ter exatamente 8 caracteres;
        - Conter pelo menos uma letra maiúscula;
        - Conter pelo menos um número;
        - Conter apenas letras e números (sem símbolos).

    Funções:
        enviar_email():
            Após a confirmação da senha, um código de verificação é enviado para o e-mail fornecid.
            O usuário deve inserir corretamente esse código para concluir a validação.

    Parâmetros:
        email (str): E-mail do usuário que receberá o código de verificação.

    Retorno:
        str: Senha validada e confirmada, se todas as etapas forem concluídas com sucesso.

    Observação:
        A função exibe mensagens de erro específicas caso a senha não atenda aos critérios, as confirmações falhem,
        ou o código de verificação esteja incorreto.
    """
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
def cadastrar_usuario():
    """
    Realiza o cadastro de um novo usuário, incluindo nome, e-mail e senha com verificação.

    Etapas do processo:
        1. Solicita o nome completo do usuário (com validação);
        2. Solicita e valida o e-mail institucional;
        3. Verifica se o e-mail já está cadastrado;
        4. Caso o e-mail seja novo, solicita a criação da senha com validação e confirmação via código;
        5. Salva os dados do usuário no arquivo de usuários.

    Funções:
        validar_nome():
            Solicita e valida o nome completo do usuário.
        validar_email():
            Solicita e valida o e-mail institucional do usuário.
        email_ja_cadastrado(email):
            Verifica se o e-mail já está cadastrado. Caso esteja, o cadastro é interrompido.
        validar_senha(email):
            Solicita a criação de uma senha segura e realiza verificação por código via e-mail.

    Retorno:
        str: E-mail do usuário cadastrado, caso o processo seja concluído com sucesso.
        None: Se o e-mail já estiver cadastrado.

    Observação:
        - Os dados são armazenados no formato: nome;email;senha;
        - Em caso de e-mail já existente, o usuário é redirecionado para o menu de login.
    """

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

    print(" Cadastro realizado com sucesso!")
    print("Limpando a tela...")
    time.sleep(2)
    limpar_terminal()
    return email

def login():
    """
    Realiza o login do usuário, diferenciando entre administrador e usuários comuns.

    Fluxo:
        1. Solicita o e-mail do usuário;
        2. Se for o e-mail do administrador, envia um código de acesso por e-mail para validação;
        3. Se o código for confirmado, o login de administrador é concluído;
        4. Para usuários comuns, solicita a senha e verifica as credenciais no arquivo de usuários;
        5. Caso as credenciais estejam corretas, o login é realizado;
        6. Em caso de falha, exibe mensagem de erro.

    Funções utilizadas:
        enviar_email(email, codigo, mensagem):
            Envia um código de verificação por e-mail para oadministrador, sendo a senha gerada para ele.
        limpar_terminal():
            Limpa a tela do terminal após o login bem-sucedido.

    Retorno:
        Retorna uma tupla, cunjunto de variáveis, com o nome e e-mail do usuário logado (ou administrador).
        None: Caso o login falhe por credenciais inválidas ou código incorreto.

    Observação:
        - Os dados dos usuários comuns são lidos do arquivo especificado em ARQUIVO_USUARIOS.
        - O administrador realiza login via código enviado por e-mail para maior segurança.
    """

    print("=== Login ===\n")
    email = input("Email: ").strip().lower()
    if email == EMAIL_ADM:
        codigo = random.randint(100000, 999999)
        mensagem = ("ótimo dia administrador, aqui está seu codigo de acesso: ")
        enviar_email(email, codigo, mensagem)
        codigo_digitado = input("Digite o código enviado ao email do administrador: ")
        if str(codigo_digitado) == str(codigo):
            print("Login de administrador bem-sucedido!")
            return (NOME_ADM, EMAIL_ADM)
        else:
            print("Código incorreto.")
            return None

    senha = input("Senha: ").strip()
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                nome, e, s = linha.strip().split(";")
                if e == email and s == senha:
                    print("Login bem-sucedido!")
                    print("Limpando a tela...")
                    time.sleep(2)
                    limpar_terminal()
                    return (nome, email)
    except FileNotFoundError:
        pass

    print(" Email ou senha inválidos.")
    return None

def listar_usuarios():
    """
    Exibe todos os usuários cadastrados no sistema, mostrando nome e e-mail.

    Fluxo:
        1. Tenta abrir o arquivo de usuários;
        2. Se o arquivo existir e houver usuários cadastrados, exibe uma lista numerada com nome e e-mail;
        3. Caso não existam usuários ou o arquivo esteja vazio, informa que não há usuários cadastrados;
        4. Aguarda o usuário pressionar uma tecla para voltar ao menu;
        5. Limpa o terminal antes de retornar.

    Funções utilizadas:
        limpar_terminal():
            Limpa a tela do terminal após exibir a lista de usuários.

    Retorno:
        None: A função apenas exibe informações, sem retornar dados.

    Observação:
        - Os dados são lidos do arquivo definido por ARQUIVO_USUARIOS;
        - Senhas não são exibidas por questões de segurança.
    """
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            usuarios = arquivo.readlines()

        if not usuarios:
            print("Nenhum usuário cadastrado ainda.")
            return

        print("\n=== Lista de Usuários Cadastrados ===\n")
        for i, linha in enumerate(usuarios, 1):
            nome, email, _ = linha.strip().split(";")
            print(f"{i}. Nome: {nome} | Email: {email}")
    except FileNotFoundError:
        print("Arquivo de usuários não encontrado.")

    input("Digite qualquer tecla para retornar ao menu.")
    print("\nVoltando ao menu...")
    time.sleep(2)
    limpar_terminal()

def excluir_usuario():
    """
    Exclui um usuário do sistema com base no e-mail informado.

    Fluxo:
        1. Solicita o e-mail do usuário a ser excluído;
        2. Lê o arquivo de usuários e filtra todas as entradas, removendo a linha correspondente ao e-mail informado;
        3. Se o e-mail for encontrado, reescreve o arquivo com os dados atualizados (sem o usuário excluido);
        4. Se o e-mail não for encontrado, informa que o usuário não existe;
        5. Em caso de erro na leitura do arquivo, apresenta o erro para o usuário;
        6. Após o processo, retorna ao menu e limpa o terminal.

    Funções utilizadas:
        limpar_terminal():
            Limpa a tela do terminal após a exclusão ou falha.

    Observação:
        - A exclusão é baseada no e-mail exato digitado pelo administrador;
        - Os dados são lidos e regravados no arquivo 'ARQUIVO_USUARIOS';
        - O formato das linhas no arquivo deve ser: nome;email;senha;
    """
    email_excluir = input("Digite o email do usuário que deseja excluir: ").strip().lower()
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            usuarios = arquivo.readlines()

        nova_lista = [linha for linha in usuarios if linha.strip().split(";")[1] != email_excluir]
# cria uma nova lista, onde percorre cada linha da lista usuarios e só adiciona na nova lista se o email for diferente do digitado para ser excluido.

        if len(nova_lista) == len(usuarios):
            print("Usuário não encontrado.")
        else:
            with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
                arquivo.writelines(nova_lista)
            print("Usuário excluído com sucesso!")
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    print("\nVoltando ao menu...")
    time.sleep(2)
    limpar_terminal()

def excluir_propria_conta(email_usuario):
    """
    Permite que o usuário exclua a própria conta, mediante confirmação e validação da senha.

    Fluxo:
        1. Solicita confirmação do usuário digitando 'SIM' para prosseguir com a exclusão;
        2. Solicita a senha para validar a identidade do usuário;
        3. Lê o arquivo de usuários e remove a linha correspondente ao e-mail e senha informados;
        4. Se a senha estiver correta, reescreve o arquivo sem os dados do usuário e confirma a exclusão;
        5. Se a senha estiver incorreta, cancela a exclusão e informa o erro;
        6. Em caso de erro na leitura ou escrita do arquivo, exibe uma mensagem de erro.

    Parâmetros:
        email_usuario (str): E-mail do usuário logado, usado para identificar qual conta excluir.

    Retorno:
        bool:
            True – se a conta for excluída com sucesso;
            False – se a exclusão for cancelada, a senha estiver incorreta ou ocorrer algum erro.

    Exceções:
            Qualquer erro ocorrido durante o processo de leitura ou escrita do arquivo será capturado, em 'e',
            exibindo uma mensagem de erro no terminal e retornando False.

    Observação:
        - A exclusão só é feita se o e-mail e a senha corresponderem exatamente a uma linha do arquivo;
        - O formato de cada linha do arquivo é: nome;email;senha.
    """

    confirmacao = input("Tem certeza que deseja excluir sua conta? Digite 'SIM' para confirmar: ").strip().upper()
    if confirmacao != "SIM":
        print(" Exclusão cancelada.")
        return False

    senha_digitada = input("Digite sua senha para confirmar: ").strip()
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            usuarios = arquivo.readlines()

        nova_lista = []
        conta_excluida = False

        for linha in usuarios:
            n, email, senha = linha.strip().split(";")
            if email == email_usuario and senha_digitada == senha:
                conta_excluida = True
            else:
                nova_lista.append(linha)

        if conta_excluida:
            with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
                arquivo.writelines(nova_lista)
            print("Sua conta foi excluída com sucesso.")
            return True
        else:
            print("Senha incorreta. Conta não foi excluída.")
            return False
    except Exception as e:
        print("Erro ao excluir conta:", e)
        return False

def alterar_dados_usuario(email_usuario):
    """
    Permite que o usuário altere seus próprios dados (nome ou senha), mediante verificação.

    Fluxo:
        1. Lê todas as linhas do arquivo de usuários;
        2. Identifica a linha correspondente ao e-mail do usuário logado;
        3. Pergunta ao usuário se deseja alterar o nome ou a senha;
        4. Caso escolha alterar o nome, solicita um novo nome com validação;
        5. Caso escolha alterar a senha, exige a senha atual como verificação e, se correta, permite definir uma nova;
        6. Reescreve o arquivo de usuários com os dados atualizados;
        7. Exibe mensagem de confirmação ao final.

    Parâmetros:
        email_usuario (str): E-mail do usuário logado, usado para localizar seus dados no arquivo.

    Exceções tratadas:
        Exception:
            Qualquer erro ocorrido durante o processo de leitura, validação ou escrita será capturado, em e,
            exibindo uma mensagem de erro no terminal.

    Observação:
        - O arquivo de usuários é reescrito por completo, com os dados atualizados apenas do usuário logado;
        - A senha só pode ser alterada se a antiga for confirmada corretamente;
        - O formato do arquivo segue: nome;email;senha.
    """

    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            usuarios = arquivo.readlines()

        nova_lista = []
        for linha in usuarios:
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
    """
    Permite ao usuário redefinir sua senha através de verificação por e-mail caso a esqueça.

    Etapas do processo:
        1. Solicita o e-mail do usuário e verifica se está cadastrado;
        2. Envia um código de verificação para o e-mail informado;
        3. O usuário tem até 3 tentativas para inserir o código corretamente;
        4. Se o código for validado, solicita uma nova senha com validação;
        5. Atualiza a senha no arquivo de usuários.
    funções:
        email_ja_cadastrado(email):
            Verifica se o e-mail informado já existe no sistema.
        enviar_email(email, codigo, mensagem):
            Envia um e-mail com o código de verificação para o usuário.
        validar_senha(email):
            Solicita a criação de uma nova senha com validações e confirma a identidade via e-mail.
        Exceções tratadas:
    Exception:
        Caso ocorra qualquer erro durante a leitura ou escrita do arquivo, em 'e',
        uma mensagem será exibida informando o problema.

    Observações:
        - A nova senha deve seguir os mesmos critérios da função `validar_senha`;
        - O código de verificação é enviado por e-mail através da função `enviar_email`;
        - O processo é cancelado após 3 tentativas incorretas de digitar o código;
        - O formato do arquivo é: nome;email;senha.
    """

    print("\n=== Redefinir Senha ===")
    email = input("Digite seu email: ").strip().lower()

    if not email_ja_cadastrado(email):
        print(" Email não encontrado.")
        return

    # Envia código de verificação
    codigo = random.randint(100000, 999999)
    mensagem = "Código para redefinição de senha:"
    enviar_email(email, codigo, mensagem)

    for tentativa in range(3):
        codigo_digitado = input("Digite o código enviado ao seu email: ").strip()
        if codigo_digitado == str(codigo):
            print(" Código correto.")
            nova_senha = validar_senha(email)

            # Atualiza a senha no arquivo
            try:
                with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
                    usuarios = arquivo.readlines()

                with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
                    for linha in usuarios:
                        nome, e, senha_antiga = linha.strip().split(";")
                        if e == email:
                            arquivo.write(f"{nome};{email};{nova_senha}\n")
                        else:
                            arquivo.write(linha)
                print("Senha redefinida com sucesso!")
                return
            except Exception as e:
                print("Erro ao redefinir senha:", e)
                return
        else:
            print(" Código incorreto. Tente novamente.")

    print("Número máximo de tentativas excedido.")

# ----------------------------
# Gereciamento de bolsas pelo ADM
# ----------------------------
def menu_gerenciar_bolsas():
    """
    Exibe o menu de gerenciamento de bolsas e direciona para as ações disponíveis de acordo com a escolha do administrador.

    Etapas do processo:
        1. Mostra um menu com as opções disponíveis para o gerenciamento de bolsas;
        2. Aguarda a escolha do usuário;
        3. Executa a função correspondente com base na opção escolhida;
        4. Permite repetir o processo até que o usuário escolha a opção de voltar.

    Funções utilizadas:
        adicionar_bolsa():
            Adiciona uma nova bolsa ao sistema.

        listar_bolsas():
            Exibe a lista de todas as bolsas cadastradas.

        editar_bolsa():
            Permite editar os dados de uma bolsa específica.

        excluir_bolsa():
            Exclui uma bolsa existente do sistema.

    Observações:
        - O menu permanece em loop até que o usuário selecione a opção "Voltar";
        - Em caso de opção inválida, uma mensagem é exibida solicitando nova tentativa.
    """
    while True:
        print("\n=== GERENCIAR BOLSAS ===")
        print("1 - Adicionar nova bolsa")
        print("2 - Listar bolsas")
        print("3 - Editar bolsa")
        print("4 - Excluir bolsa")
        print("5 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_bolsa()
        elif opcao == "2":
            listar_bolsas()
        elif opcao == "3":
            editar_bolsa()
        elif opcao == "4":
            excluir_bolsa()
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")

#--------- Funcionalidades (menu_gerenciar_bolsas) ---------

def adicionar_bolsa():
    """
    Adiciona uma nova bolsa ao sistema, coletando e validando os dados inseridos pelo usuário.

    Etapas do processo:
        1. Solicita o tipo da bolsa (Atleta, Pesquisa ou Técnica);
        2. Valida o tipo informado;
        3. Coleta e valida os seguintes dados da bolsa:
            - Título
            - Instituição
            - Valor
            - Duração
            - Instruções das atividades
            - Local das atividades
            - Número de vagas
        4. Salva as informações no arquivo de bolsas.

    Funções:
        validar_texto():
            Valida se os campos de texto contêm apenas letras, espaços e pontuação básica.
        validar_numero():
            Valida se a entrada é numérica (ex: valor da bolsa e número de vagas).

    Observações:
        - O tipo da bolsa deve ser obrigatoriamente: Atleta, Pesquisa ou Técnica;
        - Caso algum dado seja inválido, a função exibe uma mensagem e encerra a operação sem salvar;
        - As bolsas são armazenadas no formato:
            tipo;titulo;instituicao;valor;duracao;instrucoes;local;vagas
    """
    print("\n=== Adicionar Nova Bolsa ===")

    tipo = input("Tipo da bolsa (Atleta, Pesquisa, Tecnica): ").strip().lower().title()
    if tipo not in ["Atleta", "Pesquisa", "Tecnica"]:
        print("Tipo inválido.")
        return

    titulo = validar_texto("Digite o título da bolsa", vazio = False).title()
    instituicao = validar_texto("Instituição provedora da bolsa", vazio = False)
    valor = validar_numero("Valor da bolsa (em R$)", vazio = False)
    duracao = validar_texto("Digite a duração da bolsa(ex: Duas semanas, Cinco anos..)", vazio = False)
    instrucoes = validar_texto("Instruções das atividades", vazio = False)
    local = validar_texto("Local das atividades (endereço ou 'online')", vazio = False)
    vagas = validar_numero("Número de vagas disponíveis", vazio = False)

    with open(ARQUIVO_BOLSAS, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{tipo};{titulo};{instituicao};{valor};{duracao};{instrucoes};{local};{vagas}\n")

    print("Bolsa cadastrada com sucesso!")

def listar_bolsas():
    """
    Lista todas as bolsas cadastradas no sistema, exibindo os detalhes de cada uma.

    Etapas do processo:
        1. Abre o arquivo de bolsas e lê todas as linhas;
        2. Verifica se há bolsas cadastradas:
            - Se não houver, informa o usuário e encerra;
            - Se houver, exibe os dados organizados de cada bolsa.

    Exceções tratadas:
        FileNotFoundError: Caso o arquivo de bolsas não exista, uma mensagem de erro será exibida.

    Observações:
        - A função apenas exibe as informações, sem modificar o arquivo.
    """

    try:
        with open(ARQUIVO_BOLSAS, "r", encoding="utf-8") as arquivo:
            bolsas = arquivo.readlines()

        if not bolsas:
            print("Nenhuma bolsa cadastrada ainda.")
            return

        print("\n=== Lista de Bolsas ===")
        for i, linha in enumerate(bolsas, 1):
            tipo, titulo, instituicao, valor, duracao, instrucoes, local, vagas = linha.strip().split(";")
            print(f"\n{i}. Tipo: {tipo.capitalize()}")
            print(f"   Titulo: {titulo}")
            print(f"   Instituição: {instituicao}")
            print(f"   Valor: R${valor}")
            print(f"   Duração: {duracao}")
            print(f"   Instruções: {instrucoes}")
            print(f"   Local: {local}")
            print(f"   Vagas: {vagas}")
    except FileNotFoundError:
        print("Arquivo de bolsas não encontrado.")

def editar_bolsa():
    """
    Permite ao administrador editar os dados de uma bolsa já cadastrada no sistema.

    Etapas do processo:
        1. Lista os títulos das bolsas disponíveis usando a função `listar_titulos_bolsas()`;
        2. Solicita ao administrador o número da bolsa que deseja editar;
        3. Para cada campo da bolsa (exceto o tipo), solicita um novo valor:
            - Se o campo for deixado em branco (apertar Enter), mantém o valor anterior;
        4. Substitui os dados antigos pela nova linha modificada;
        5. Reescreve o arquivo com a lista atualizada de bolsas.

    Funções utilizadas:
        - listar_titulos_bolsas():
            Retorna uma lista com todas as linhas (bolsas) do arquivo para permitir a seleção.
        - validar_texto(mensagem, vazio=True/False):
            Solicita e valida textos como título, instituição, duração, instruções e local.
        - validar_numero(mensagem, vazio=True/False):
            Solicita e valida valores numéricos como valor da bolsa e número de vagas.

    Exceções tratadas:
        - ValueError: Caso o número digitado não seja um inteiro válido.

    Observações:
        - O operador Walrus (`:=`) é utilizado para simplificar a atribuição condicional dos novos valores;
        - Apenas os campos editáveis são atualizados. O tipo da bolsa não é alterado nesta função.
    """

    bolsas = listar_titulos_bolsas()
    if not bolsas:
        return

    try:
        escolha = int(input("Digite o número da bolsa que deseja editar: "))
        if escolha < 1 or escolha > len(bolsas):
            print("Número inválido.")
            return

        dados = bolsas[escolha - 1].strip().split(";")
        print("\n=== Editar Bolsa ===")
        print("Digite Enter se desar manter o valor anterior\n")

        if (novo_titulo := validar_texto(f"Título ({dados[1]})", vazio = True)) is None: #Operador Walrus(':=')
            novo_titulo = dados[1]
        if (nova_instituicao := validar_texto(f"Instituição ({dados[2]})", vazio = True)) is None:
            nova_instituicao = dados[2]
        if (novo_valor := validar_numero(f"Valor ({dados[3]})", vazio = True)) is None:
            novo_valor = dados[3]
        if (nova_duracao := validar_texto(f"Duração ({dados[4]}", vazio = True)) is None:
            nova_duracao = dados[4]
        if (novas_instrucoes := validar_texto(f"Instruções ({dados[5]})", vazio = True)) is None:
            novas_instrucoes = dados[5]
        if (novo_local := validar_texto(f"Local ({dados[6]})", vazio = True)) is None:
            novo_local = dados[6]
        if (novas_vagas := validar_numero(f"Vagas ({dados[7]})", vazio = True)) is None:
            novas_vagas = dados[7]

        nova_linha = f"{dados[0]};{novo_titulo};{nova_instituicao};{novo_valor};{nova_duracao};{novas_instrucoes};{novo_local};{novas_vagas}\n"
        bolsas[escolha - 1] = nova_linha

        with open(ARQUIVO_BOLSAS, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(bolsas)

        print("Bolsa atualizada com sucesso!")

    except ValueError:
        print("Entrada inválida.")

def excluir_bolsa():
    """
    Exclui uma bolsa cadastrada com base na escolha do usuário.

    Etapas do processo:
        1. Lista todas as bolsas disponíveis usando a função `listar_titulos_bolsas()`;
        2. Solicita ao usuário que escolha a bolsa a ser excluída pelo número da lista;
        3. Verifica se a escolha é válida (número dentro do intervalo);
        4. Solicita confirmação do usuário antes de excluir;
        5. Remove a bolsa da lista e reescreve o arquivo com os dados atualizados.

    Funções utilizadas:
        - listar_titulos_bolsas():
            Retorna todas as linhas do arquivo de bolsas, usadas para exibir e selecionar.

    Exceções tratadas:
        - ValueError: Caso o valor digitado para a escolha não seja um número inteiro.

    Observações:
        - A exclusão é feita apenas se o usuário confirmar com "s";
        - O sistema regrava o arquivo `ARQUIVO_BOLSAS` com as bolsas restantes.
    """

    bolsas = listar_titulos_bolsas()
    if not bolsas:
        return

    try:
        escolha = int(input("Digite o número da bolsa que deseja excluir: "))
        if escolha < 1 or escolha > len(bolsas):
            print("Número inválido.")
            return

        confirma = input("Tem certeza que deseja excluir essa bolsa? (s/n): ").strip().lower()
        if confirma != "s":
            print("Operação cancelada.")
            return

        del bolsas[escolha - 1]

        with open(ARQUIVO_BOLSAS, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(bolsas)

        print("Bolsa excluída com sucesso!")

    except ValueError:
        print("Entrada inválida.")

# ----------------------------
# Vizualização das bolsa pelo usuário
# ----------------------------
def menu_bolsas(nome):
    """
    Exibe um menu interativo para que o usuário visualize bolsas disponíveis.

    Parâmetros:
        nome (str): Nome do usuário que está acessando o menu.

    Etapas do processo:
        1. Apresenta ao usuário um menu com duas opções:
            - Visualizar bolsas disponíveis;
            - Sair do menu.
        3. Repete o menu até que o usuário escolha a opção de sair.

    Funções utilizadas:
        - listar_bolsas():
            Exibe as bolsas cadastradas no sistema, com todos os detalhes.

    Observações:
        - O menu é repetido em loop enquanto a opção escolhida for inválida ou diferente de "2";
    """

    while True:
        print(f"\nEssas são as bolsas disponiveis no momento {nome}")
        print("1 - Vizualizar bolsas disponiveis")
        print("2 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_bolsas()
        elif opcao == "2":
            break
        else:
            print("opção inalida. Tente novamente")

# ----------------------------
# Menus Principais (ADM e usuário)
# ----------------------------
def menu_adm():
    """
    Exibe o menu principal para o administrador do sistema.

    Este menu oferece opções para que o administrador gerencie tanto o sistema de usuários
    quanto as bolsas disponíveis, além de permitir a saída do painel administrativo.

    Etapas do processo:
        1. Mostra o menu com três opções:
            - Gerenciar Sistema: Acessa funções relacionadas aos usuários.
            - Gerenciar Bolsas: Acessa o gerenciamento de bolsas cadastradas no sistema.
            - Sair.
        3. Continua exibindo o menu até que a opção de sair seja escolhida.

    Funções:
        - menu_gerenciar_sistema():
            Menu com opções de gerenciamento de usuários (cadastro, excluir etc).
        - menu_gerenciar_bolsas():
            Menu com opções de gerenciamento de bolsas (cadastro, listagem etc).
    """

    while True:
        print("=== MENU ADMINISTRADOR ===\n"
        "1 - Gerenciar Sistema\n"
        "2 - Gerenciar Bolsas\n"
        "3 - Sair\n")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_gerenciar_sistema()
        elif opcao == "2":
            menu_gerenciar_bolsas()
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")

def menu_usuario(nome, email):
    """
    Exibe o menu principal para um usuário comum do sistema.

    Este menu permite ao usuário acessar as configurações da sua conta, visualizar bolsas disponíveis
    ou encerrar a sessão.

    Parâmetros:
        nome (str): Nome do usuário logado.
        email (str): Email do usuário logado.

    Etapas do processo:
        1. Exibe três opções principais:
            - Configurações: Permite ao usuário editar seu nome, senha ou excluir sua conta.
            - Bolsas: Exibe as bolsas cadastradas disponíveis.
            - Sair.
        3. Atualiza o nome do usuário, caso ele seja alterado nas configurações.
        4. Continua mostrando o menu até que o usuário escolha sair.

    Funções:
        - menu_configuracoes(nome, email):
            Abre o submenu de configurações da conta do usuário (editar, excluir, etc).
            Retorna o nome atualizado caso o usuário o altere.
        - menu_bolsas(nome):
            Lista todas as bolsas disponíveis para visualização.
    """
    while True:
        print(f"\nBem-vindo, {nome}!")
        print("1 - Configurações")
        print("2 - Bolsas")
        print("3 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = menu_configuracoes(nome, email)  # atualiza o nome que foi alterado no editar dados.
        elif opcao == "2":
            menu_bolsas(nome)
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")

# ----------------------------
#Menus de Crud (usuário e ADM)
#-----------------------------
def menu_configuracoes(nome, email):
    """
    Menu de configurações pra usuário logado gerenciar sua conta.

    Aqui o usuário pode:
    1. Ver suas infos (nome e email).
    2. Alterar seus dados (nome ou senha).
    3. Excluir sua conta (com confirmação e segurança).
    4. Voltar pro menu anterior.

    Parâmetros:
        nome (str): Nome do usuário atual.
        email (str): Email do usuário atual.

    Funções:
        - alterar_dados_usuario(email):
            Permite editar nome ou senha.
        - excluir_propria_conta(email):
            Faz o processo seguro de excluir a conta.
        - limpar_terminal():
            Limpa a tela pra deixar tudo clean.
        - menu_login_cadastro():
            Redireciona pra tela inicial de login/cadastro.
        - time.sleep(): Dá uma pausa no código.
    """

    while True:
        print("\n=== CONFIGURAÇÕES ===")
        print("1 - Ver minhas informações")
        print("2 - Alterar meus dados")
        print("3 - Excluir minha conta")
        print("4 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print(f"\nNome: {nome}")
            print(f"Email: {email}")
        elif opcao == "2":
            alterar_dados_usuario(email)
        elif opcao == "3":
            if excluir_propria_conta(email):
                print("Encerrando sessão...")
                time.sleep(2)
                limpar_terminal()
                menu_login_cadastro()
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")

def menu_gerenciar_sistema():
    """
    Exibe o menu de gerenciamento do sistema de usuários, permitindo cadastro, listagem e exclusão.

    Opções do menu:
        1 - Cadastrar novo usuário: chama a função para realizar o cadastro.
        2 - Listar usuários: exibe todos os usuários cadastrados.
        3 - Excluir usuário: permite excluir um usuário pelo email.
        4 - Voltar: retorna ao menu anterior.

    Funcionamento:
        O menu roda em loop até o administrador escolher a opção de voltar.
        Valida a opção escolhida e executa a função correspondente.
        Exibe mensagem de opção inválida caso o administrador digite algo fora do esperado.

    Funções:
        cadastrar_usuario():
            Realiza o cadastro de um novo usuário com validações.
        listar_usuarios():
            Lista todos os usuários cadastrados no sistema.
        excluir_usuario():
            Exclui um usuário existente a partir do email informado.
    """

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
# Execução Principal (Login e cadastro)
# ----------------------------
def menu_login_cadastro():
    """
    Exibe o menu inicial do sistema, permitindo ao usuário realizar login, cadastro, redefinir senha ou sair.

    Opções do menu:
        1 - Login: chama a função de login para autenticar o usuário.
        2 - Cadastrar-se: chama a função para cadastrar novo usuário.
        3 - Redefinir senha: inicia o processo de recuperação de senha via email.
        4 - Sair: encerra o programa.

    Funcionamento:
        Após limpar a tela, o menu roda em loop até o usuário escolher sair.
        Se o login for bem-sucedido, direciona para o menu do administrador ou do usuário comum.
        Valida as opções digitadas e chama as funções correspondentes.
        Exibe mensagem de erro para opção inválida.

    Funções:
        limpar_terminal():
            Limpa a tela do terminal para melhor visualização.
        login():
            Realiza a autenticação do usuário, retornando nome e email se bem-sucedido.
        cadastrar_usuario():
            Realiza o cadastro de um novo usuário no sistema.
        redefinir_senha():
            Permite o usuário redefinir sua senha após confirmação via email.
        menu_adm():
            Menu principal para o administrador gerenciar o sistema e bolsas.
        menu_usuario(nome, email):
            Menu principal para o usuário comum acessar configurações e bolsas.
    """
    limpar_terminal()
    while True:
        print("Uni Bolsas UFRPE\n"
        "1 - Login\n"
        "2 - Cadastrar-se\n"
        "3 - Redefinir senha\n"
        "4 - Sair\n")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            resultado_log = login()
            if resultado_log:
                nome, email = resultado_log
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
