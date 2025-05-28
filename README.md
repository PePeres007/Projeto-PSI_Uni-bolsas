# 🎓 UniBolsas UFRPE

**UniBolsas** é uma aplicação terminal em Python criada para gerenciar usuários e bolsas acadêmicas da UFRPE. O projeto está em desenvolvimento e conta com funcionalidades de cadastro, login, autenticação por email, gerenciamento de contas e também com um sistema completo de cadastro e controle de bolsas.

---

## 📦 Funcionalidades

- Cadastro com validação de nome, email e senha  
- Verificação por código enviado por email  
- Login de usuário comum e administrador  
- Alteração de dados, exclusão de conta e redefinição de senha  
- Armazenamento de dados em arquivos `.txt`  
- Gerenciamento de bolsas (CRUD) para administradores  
- Visualização de bolsas disponíveis para usuários  

---

## 🧠 Estrutura do Projeto

```
├── UNIBOLSAS.py          # Código-fonte principal
├── usuarios.txt           # Base de dados local de usuários
├── bolsas.txt             # Base de dados local das bolsas cadastradas
└── README.md              # Documentação do projeto
```

---

## ⚙️ Módulos e para que servem

| Módulo         | Função no Projeto                                                                 |
|----------------|------------------------------------------------------------------------------------|
| `os`           | Limpa o terminal com `os.system('cls' ou 'clear')` para manter o visual limpo     |
| `re`           | Realiza validações com expressões regulares (ex: nome, email, senha)          |
| `random`       | Gera códigos aleatórios de verificação de 6 dígitos para autenticação              |
| `time`         | Introduz pausas temporárias (como `sleep(2)`) para melhor fluxo no terminal    |
| `smtplib`      | Conecta ao servidor SMTP do Gmail para envio de emails                            |
| `email.message.EmailMessage` | Cria e formata a mensagem de email enviada ao usuário               |

---

## 🚀 Como Executar nosso programa

1. **Clone o repositório:**

```bash
git clone https://github.com/PePeres007/Projeto-PSI_Uni-bolsas.git
cd unibolsas
```

2. **Execute o programa no terminal:**

```bash
python "unibolsas.py"
```

---

## 💻 Usuários e Administradores

- **Usuário comum:**
  - Faz cadastro com verificação por email
  - Visualiza informações de bolsas cadastradas
  - Acessa painel de configurações pessoais

- **Administrador:**
  - Login com verificação por uma senha já pré definida por email
  - Acessa dois menus principais:
    - **Gerenciar Sistema:** cadastrar, listar e excluir usuários
    - **Gerenciar Bolsas:** adicionar, editar, excluir e listar bolsas acadêmicas

---

## 📂 Funcionalidades de Bolsa (ADM)

- `adicionar_bolsa()`: Cria nova bolsa com dados como tipo, valor, local, duração, etc.  
- `listar_bolsas()`: Mostra uma lista completa de todas as bolsas cadastradas  
- `editar_bolsa()`: Permite atualizar os dados de uma bolsa existente  
- `excluir_bolsa()`: Remove uma bolsa do sistema com confirmação  

---

## 🔍 Visualização de Bolsas (Usuário)

- Através do menu `menu_bolsas()`, os usuários podem:
  - Ver a lista completa das bolsas cadastradas
  - Acessar todos os detalhes: tipo, valor, duração, local, vagas etc.

---

## 📌 Requisitos necessários

- Python 3.x  
- Acesso à internet para envio de email  
- Conta Gmail com senha de app gerada  

---

## 💡 Possíveis futuras melhorias

- Interface gráfica  
- Versão web  
- Simulador de aptidão de auxílio moradia através do CEP do usuário  
- Sistema de notificação por email sobre novas oportunidades    

---

## 👥 Autores

- Pedro Peres Benicio  
- Igor Dias Vieira
