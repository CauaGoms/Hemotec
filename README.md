# 🩸 Hemotec - Sistema de Gestão de Doação de Sangue

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow.svg)

Sistema web completo para gerenciamento de doações de sangue, unidades de coleta, campanhas e estoque de hemocomponentes.

[Características](#-características) •
[Tecnologias](#-tecnologias) •
[Instalação](#-instalação) •
[Uso](#-uso) •
[Documentação](#-documentação)

</div>

---

## 📋 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Características](#-características)
- [Tecnologias](#-tecnologias)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Testes](#-testes)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Documentação](#-documentação)
- [Contribuição](#-contribuição)
- [Licença](#-licença)
- [Contato](#-contato)

---

## 🎯 Sobre o Projeto

**Hemotec** é um sistema web desenvolvido para otimizar o processo de doação de sangue, conectando doadores, unidades de coleta e gestores em uma plataforma integrada. O sistema permite:

- **Gestão completa** de doadores e doações
- **Controle de estoque** de hemocomponentes
- **Agendamento inteligente** de doações
- **Campanhas de captação** de doadores
- **Relatórios gerenciais** detalhados
- **Notificações automáticas** via email
- **Sistema de licenciamento** por assinatura

---

## ✨ Características

### 👥 Perfis de Usuário

#### 🩸 **Doador**
- Cadastro completo com histórico médico
- Agendamento de doações online
- Visualização de histórico de doações
- Carteira digital do doador
- Notificações de campanhas
- Acompanhamento de resultados de exames

#### 🏥 **Colaborador**
- Registro de doações e triagens
- Gestão de agendamentos
- Controle de campanhas locais
- Anexação de resultados de exames
- Gerenciamento de disponibilidade da unidade

#### 👨‍💼 **Administrador de Unidade**
- Gestão de colaboradores
- Relatórios de estoque e doações
- Controle de campanhas da unidade
- Análise por tipo sanguíneo e período
- Configuração de horários de funcionamento

#### 🎯 **Gestor Institucional**
- Visão geral de múltiplas unidades
- Relatórios consolidados
- Gestão de administradores
- Controle de licenças e assinaturas
- Análise de indicadores estratégicos

### 🔒 Segurança
- Autenticação com bcrypt
- Sessões seguras com middleware
- Validação de dados com Pydantic
- Proteção contra SQL Injection
- Hash de senhas com SHA-256 + bcrypt
- Sistema de recuperação de senha

### 📊 Funcionalidades Avançadas
- **API RESTful** para integração externa
- **Geração de PDF** para relatórios e carteiras
- **Sistema de notificações** por email
- **Validação de CEP** e localização
- **Upload de documentos** e resultados
- **Controle de estoque** em tempo real

---

## 🛠 Tecnologias

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[Python 3.9+](https://www.python.org/)** - Linguagem de programação
- **[SQLite](https://www.sqlite.org/)** - Banco de dados
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Validação de dados
- **[Jinja2](https://jinja.palletsprojects.com/)** - Template engine

### Segurança & Autenticação
- **[bcrypt](https://github.com/pyca/bcrypt/)** - Hash de senhas
- **[python-jose](https://github.com/mpdavis/python-jose)** - JWT tokens
- **[passlib](https://passlib.readthedocs.io/)** - Gerenciamento de senhas

### Utilitários
- **[ReportLab](https://www.reportlab.com/)** - Geração de PDFs
- **[Resend](https://resend.com/)** - Serviço de email
- **[Pillow](https://pillow.readthedocs.io/)** - Processamento de imagens
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Variáveis de ambiente

### Testes
- **[pytest](https://pytest.org/)** - Framework de testes
- **[pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)** - Testes assíncronos
- **[pytest-cov](https://pytest-cov.readthedocs.io/)** - Cobertura de código

---

## 🏗 Arquitetura

O projeto segue uma arquitetura em camadas (Layered Architecture):

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│    (Routes/Templates/Static)        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Application Layer           │
│      (DTOs/Validators/Utils)        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│          Business Layer             │
│          (Repositories)             │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│           Data Layer                │
│       (Models/Database)             │
└─────────────────────────────────────┘
```

**Veja mais detalhes em:** [ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 📦 Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/CauaGoms/Hemotec.git
cd Hemotec
```

### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações do Servidor
HOST=127.0.0.1
PORT=8000
DEBUG=True

# Segurança
SECRET_KEY=sua_chave_secreta_super_segura_aqui

# Banco de Dados
DATABASE_PATH=dados.db
TEST_DATABASE_PATH=test_dados.db

# Email
RESEND_API_KEY=sua_chave_api_resend
EMAIL_FROM=noreply@seudominio.com
EMAIL_FROM_NAME=Hemotec

# API Externa (Localização)
VIACEP_API_URL=https://viacep.com.br/ws
```

**⚠️ Importante:** Nunca commite o arquivo `.env` no repositório!

---

## 💻 Uso

### Executar o servidor de desenvolvimento

```bash
# Método 1: Via Python
python main.py

# Método 2: Via Uvicorn
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

O sistema estará disponível em: `http://127.0.0.1:8000`

### Acessar a aplicação

- **Página Inicial:** http://127.0.0.1:8000
- **Login:** http://127.0.0.1:8000/login
- **Cadastro de Doador:** http://127.0.0.1:8000/cadastrar
- **Documentação da API:** http://127.0.0.1:8000/docs (Swagger UI)

### Usuários padrão (desenvolvimento)

```
Doador:
- Email: doador@gmail.com
- Senha: #Doador123

Colaborador:
- Email: colaborador@gmail.com
- Senha: #Colaborador123

Administrador:
- Email: administrador@gmail.com
- Senha: #Administrador123

Gestor:
- Email: gestor@gmail.com
- Senha: #Gestor123
```

---

## 🧪 Testes

### Executar todos os testes

```bash
pytest
```

### Executar com cobertura

```bash
pytest --cov=. --cov-report=html
```

### Executar testes específicos

```bash
# Testar apenas repositórios
pytest tests/test_*_repo.py

# Testar um módulo específico
pytest tests/test_usuario_repo.py

# Executar com verbose
pytest -v
```

---

## 📁 Estrutura do Projeto

```
Hemotec/
├── data/                      # Camada de dados
│   ├── model/                # Modelos de entidades
│   ├── repo/                 # Repositórios (acesso ao BD)
│   └── sql/                  # Scripts SQL
├── dtos/                      # Data Transfer Objects
├── routes/                    # Rotas da aplicação
│   ├── publico/              # Rotas públicas
│   ├── doador/               # Rotas do doador
│   ├── colaborador/          # Rotas do colaborador
│   ├── adm_unidade/          # Rotas do administrador
│   ├── gestor/               # Rotas do gestor
│   ├── api/                  # APIs REST
│   └── auth_routes.py        # Autenticação
├── templates/                 # Templates HTML (Jinja2)
├── static/                    # Arquivos estáticos
│   ├── css/                  # Estilos
│   ├── js/                   # Scripts JavaScript
│   └── img/                  # Imagens
├── util/                      # Utilitários
│   ├── auth_decorator.py     # Decoradores de autenticação
│   ├── database.py           # Conexão com banco
│   ├── security.py           # Funções de segurança
│   ├── email_service.py      # Serviço de email
│   └── pdf_generator.py      # Geração de PDFs
├── tests/                     # Testes automatizados
├── main.py                    # Ponto de entrada
├── requirements.txt           # Dependências
├── pytest.ini                # Configuração do pytest
├── Dockerfile                # Container Docker
└── README.md                 # Este arquivo
```

---

## 📚 Documentação

- **[Arquitetura](docs/ARCHITECTURE.md)** - Detalhes da arquitetura do sistema
- **[API](docs/API_DOCS.md)** - Documentação completa da API REST
- **[Contribuição](CONTRIBUTING.md)** - Guia para contribuidores
- **[Segurança](SECURITY.md)** - Políticas de segurança

---

## 🤝 Contribuição

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre como contribuir com o projeto.

### Processo de contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📧 Contato

**Equipe Hemotec**
- GitHub: [@CauaGoms](https://github.com/CauaGoms)
- Email: contato@hemotec.com.br

---

## 🙏 Agradecimentos

- Comunidade FastAPI
- Contribuidores do projeto
- Hemocentros parceiros

---

## 📌 Roadmap

### Versão Atual (v1.0)
- [x] Sistema de autenticação
- [x] Cadastro de doadores
- [x] Agendamento de doações
- [x] Controle de estoque
- [x] Campanhas de doação

### Próximas Versões

#### v1.1 (Em Desenvolvimento)
- [ ] Sistema de notificações push
- [ ] Aplicativo mobile
- [ ] Integração com sistemas hospitalares
- [ ] Dashboard analytics avançado

#### v1.2 (Planejado)
- [ ] Machine Learning para previsão de demanda
- [ ] Sistema de pontos e gamificação
- [ ] Integração com redes sociais
- [ ] API pública para desenvolvedores

---

## ⚠️ Tarefas Técnicas Pendentes

### Alta Prioridade
- [ ] Implementar reutilização de cursor em repositórios
- [ ] Revisar e atualizar todos os testes unitários
- [ ] Implementar tratamento de erro quando API externa cair
- [ ] Adicionar fallback para funcionalidade de estoque

### Média Prioridade
- [ ] Refatorar rotas de autenticação (auth_routes.py)
- [ ] Padronizar assinaturas de funções (`usuario_logado: dict = None`)
- [ ] Adicionar inserts de dados de exemplo no banco
- [ ] Implementar logging estruturado

### Baixa Prioridade
- [ ] Melhorar cobertura de testes
- [ ] Documentar código com docstrings
- [ ] Otimizar queries do banco de dados
- [ ] Implementar cache

---

<div align="center">

**Feito com ❤️ pela equipe Hemotec**

⭐ Se este projeto foi útil, considere dar uma estrela!

</div>