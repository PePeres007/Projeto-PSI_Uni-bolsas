# Projeto PSI/ Primeiro período 
# 🎓 UniBolsas UFRPE

**UniBolsas** é uma aplicação terminal em Python criada para gerenciar usuários com foco em bolsas acadêmicas da UFRPE. O projeto está em estágio inicial, funcionando via terminal, mas já conta com cadastro, login, redefinição de senha e envio de código por email.

---

## 📦 Funcionalidades

- Cadastro com validação de nome, email e senha
- Verificação por **código enviado por email**
- Login de usuário comum e administrador
- Alteração de dados, exclusão de conta e redefinição de senha
- Sistema simples de persistência usando arquivo `.txt`
- Menus adaptados para usuários e administradores

---

## 🧠 Estrutura do Projeto

```
├── Main - Copia.py        # Código-fonte principal
├── usuarios.txt           # Base de dados local de usuários
└── README.md              # Documentação do projeto
```

---

## ⚙️ Módulos e para que servem

| Módulo                       | Função no Projeto                                                               |
| ---------------------------- | ------------------------------------------------------------------------------- |
| `os`                         | Limpa o terminal com `os.system('cls' ou 'clear')` para manter o visual limpo   |
| `re`                         | Realiza **validações com expressões regulares** (ex: nome, email, senha)        |
| `random`                     | Gera códigos aleatórios de verificação de 6 dígitos para autenticação           |
| `time`                       | Introduz **pausas temporárias** (como `sleep(2)`) para melhor fluxo no terminal |
| `smtplib`                    | Responsável por conectar ao servidor SMTP do Gmail e enviar emails              |
| `email.message.EmailMessage` | Cria e formata a mensagem de email que será enviada ao usuário                  |

---

## 🚀 Como Executar

1. **Clone o repositório (ou salve os arquivos):**

```bash
git clone https://github.com/seu-usuario/unibolsas.git
cd unibolsas
```

2. **Configure o envio de emails:**

- Crie uma senha de aplicativo no Gmail
- Substitua as seguintes variáveis no topo do código:

```python
EMAIL_REMETENTE = "seu_email@gmail.com"
SENHA_APP = "sua_senha_de_app"
EMAIL_ADM = "email_do_administrador@gmail.com"
NOME_ADM = "Nome do Administrador"
```

3. **Execute o programa no terminal:**

```bash
python "Main - Copia.py"
```

---

## 👨‍💻 Sobre usuários

- **Usuário comum:**

  - Faz cadastro com verificação por email
  - Acessa menu com opções de configurações pessoais

- **Administrador:**
  - Faz login via código pré definido por email
  - Acessa painel para listar, cadastrar e excluir usuários

---

## 📌 Requisitos

- Python 3.x
- Acesso à internet para envio de email
- Conta Gmail com senha de app gerada

---

## 💡 Possíveis futuras melhorias

- Interface gráfica
- Versão web com Flask ou Django
- Sistema de notificação por email sobre novas bolsas

---

## 👥 Autores

- Pedro Peres Benicio
- Igor Dias Vieira
