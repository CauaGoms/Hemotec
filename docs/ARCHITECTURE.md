# 🏗️ Arquitetura do Sistema Hemotec

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura em Camadas](#arquitetura-em-camadas)
- [Modelo de Dados](#modelo-de-dados)
- [Fluxo de Autenticação](#fluxo-de-autenticação)
- [Padrões de Projeto](#padrões-de-projeto)
- [Diagrams de Sistema](#diagramas-de-sistema)
- [Decisões Arquiteturais](#decisões-arquiteturais)

---

## 🎯 Visão Geral

O Hemotec é construído usando uma **arquitetura em camadas** (Layered Architecture) com FastAPI, seguindo princípios de:

- **Separação de Responsabilidades** (SoC)
- **Injeção de Dependências** (DI)
- **Repository Pattern**
- **DTO Pattern** (Data Transfer Objects)
- **MVC adaptado** para web APIs

### Stack Tecnológico

```
┌─────────────────────────────────────────┐
│         Frontend (Templates)            │
│     Jinja2 + HTML + CSS + JavaScript    │
└──────────────┬──────────────────────────┘
               │ HTTP/HTTPS
┌──────────────▼──────────────────────────┐
│         Backend (FastAPI)               │
│     Python 3.9+ + Uvicorn ASGI          │
└──────────────┬──────────────────────────┘
               │ SQL
┌──────────────▼──────────────────────────┐
│      Banco de Dados (SQLite)            │
│     Persistência de Dados               │
└─────────────────────────────────────────┘
```

---

## 🧱 Arquitetura em Camadas

### Diagrama de Camadas

```
┌───────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                     │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Routes    │  │  Templates   │  │    Static    │ │
│  │  (FastAPI)  │  │   (Jinja2)   │  │  (CSS/JS)    │ │
│  └─────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────────┬──────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────┐
│               APPLICATION LAYER                        │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │    DTOs     │  │  Validators  │  │    Utils     │ │
│  │ (Pydantic)  │  │   (Custom)   │  │  (Helpers)   │ │
│  └─────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────────┬──────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────┐
│                 BUSINESS LAYER                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │           Repositories                          │  │
│  │  (Lógica de Negócio + Acesso a Dados)          │  │
│  └─────────────────────────────────────────────────┘  │
└────────────────────────┬──────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────┐
│                   DATA LAYER                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Models    │  │   Database   │  │     SQL      │ │
│  │ (Entities)  │  │ (Connection) │  │  (Queries)   │ │
│  └─────────────┘  └──────────────┘  └──────────────┘ │
└───────────────────────────────────────────────────────┘
```

### 1. **Presentation Layer** (Camada de Apresentação)

**Responsabilidade:** Interação com o usuário

**Componentes:**

#### `routes/` - Rotas FastAPI
```python
# Exemplo: routes/doador/doador.py
@router.get("/doador")
@requer_autenticacao(["doador"])
async def get_doador_home(request: Request, usuario_logado: dict = None):
    """Página inicial do doador"""
    return templates.TemplateResponse(
        "doador/doador_inicio.html",
        {"request": request, "usuario": usuario_logado}
    )
```

**Organização das Rotas:**
```
routes/
├── publico/           # Acesso sem autenticação
├── doador/            # Rotas do doador
├── colaborador/       # Rotas do colaborador
├── adm_unidade/       # Rotas do administrador
├── gestor/            # Rotas do gestor
├── api/               # APIs REST públicas
└── auth_routes.py     # Autenticação centralizada
```

#### `templates/` - Views Jinja2
```html
<!-- Exemplo: templates/doador/doador_inicio.html -->
{% extends "components/base.html" %}

{% block content %}
<div class="container">
    <h1>Bem-vindo, {{ usuario.nome }}</h1>
    <!-- Conteúdo específico do doador -->
</div>
{% endblock %}
```

#### `static/` - Recursos estáticos
```
static/
├── css/               # Estilos CSS
├── js/                # Scripts JavaScript
├── img/               # Imagens
└── uploads/           # Arquivos enviados
```

---

### 2. **Application Layer** (Camada de Aplicação)

**Responsabilidade:** Validação e transformação de dados

#### `dtos/` - Data Transfer Objects
```python
# dtos/usuario_dtos.py
from pydantic import BaseModel, EmailStr, validator
from datetime import date

class CriarUsuarioDTO(BaseModel):
    """DTO para criação de usuário"""
    nome: str
    email: EmailStr
    cpf: str
    senha: str
    confirmar_senha: str
    data_nascimento: date
    
    @validator('confirmar_senha')
    def senhas_devem_coincidir(cls, v, values):
        if 'senha' in values and v != values['senha']:
            raise ValueError('Senhas não coincidem')
        return v
    
    @validator('cpf')
    def validar_cpf(cls, v):
        # Lógica de validação de CPF
        return v
```

**Benefícios dos DTOs:**
- ✅ Validação automática de dados
- ✅ Conversão de tipos
- ✅ Documentação clara do que é esperado
- ✅ Mensagens de erro consistentes

#### `util/` - Utilitários
```python
# util/security.py
def criar_hash_senha(senha: str) -> str:
    """Cria hash bcrypt da senha"""
    pass

# util/email_service.py
def enviar_email(para: str, assunto: str, corpo: str):
    """Envia email via Resend"""
    pass

# util/auth_decorator.py
def requer_autenticacao(perfis: list = None):
    """Decorator para proteger rotas"""
    pass
```

---

### 3. **Business Layer** (Camada de Negócio)

**Responsabilidade:** Lógica de negócio e regras da aplicação

#### `data/repo/` - Repositories

**Pattern Repository:** Abstrai o acesso aos dados

```python
# data/repo/doador_repo.py
from data.model.doador_model import Doador
from util.database import get_connection

def obter_por_id(doador_id: int) -> Doador:
    """
    Obtém doador por ID
    
    Business Rules:
    - Doador deve existir
    - Doador deve estar ativo
    """
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT * FROM doador WHERE cod_doador = ? AND status = 1
    """, (doador_id,))
    
    row = cursor.fetchone()
    conexao.close()
    
    if row:
        return Doador(**dict(row))
    return None


def pode_doar(doador_id: int) -> tuple[bool, str]:
    """
    Verifica se doador pode fazer doação
    
    Business Rules:
    - Idade entre 16 e 69 anos
    - Peso >= 50kg
    - Última doação há mais de 60 dias (homens) ou 90 dias (mulheres)
    - Sem impedimentos de saúde
    
    Returns:
        (pode_doar, mensagem)
    """
    doador = obter_por_id(doador_id)
    
    if not doador:
        return False, "Doador não encontrado"
    
    # Validar idade
    idade = calcular_idade(doador.data_nascimento)
    if idade < 16 or idade > 69:
        return False, "Idade fora do permitido (16-69 anos)"
    
    # Validar peso
    if doador.peso < 50:
        return False, "Peso mínimo não atingido (50kg)"
    
    # Validar intervalo entre doações
    ultima_doacao = obter_ultima_doacao(doador_id)
    if ultima_doacao:
        dias_desde_ultima = (date.today() - ultima_doacao.data).days
        intervalo_minimo = 60 if doador.genero == 'M' else 90
        
        if dias_desde_ultima < intervalo_minimo:
            return False, f"Aguarde {intervalo_minimo - dias_desde_ultima} dias"
    
    return True, "Apto para doação"
```

**Benefícios do Repository Pattern:**
- ✅ Centraliza lógica de acesso aos dados
- ✅ Facilita testes (mock do repositório)
- ✅ Permite trocar banco de dados facilmente
- ✅ Evita repetição de queries

---

### 4. **Data Layer** (Camada de Dados)

**Responsabilidade:** Persistência e estrutura de dados

#### `data/model/` - Modelos de Entidades

```python
# data/model/doador_model.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Doador:
    """Modelo de dados do Doador"""
    cod_doador: int
    cod_usuario: int
    tipo_sanguineo: str
    fator_rh: str
    peso: float
    altura: float
    ultima_doacao: Optional[date]
    total_doacoes: int
    status_doacao: str  # apto, inapto_temporario, inapto_permanente
    observacoes: Optional[str]
    
    def __post_init__(self):
        """Validações após inicialização"""
        if self.tipo_sanguineo not in ['A', 'B', 'AB', 'O']:
            raise ValueError("Tipo sanguíneo inválido")
        
        if self.fator_rh not in ['+', '-']:
            raise ValueError("Fator RH inválido")
```

#### `util/database.py` - Conexão com Banco

```python
import sqlite3
import os

def get_connection():
    """
    Obtém conexão com banco de dados
    
    Features:
    - Suporta banco de testes via variável de ambiente
    - Habilita foreign keys
    - Retorna rows como dicionários
    """
    database_path = os.environ.get('TEST_DATABASE_PATH', 'dados.db')
    conexao = sqlite3.connect(database_path)
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.row_factory = sqlite3.Row
    return conexao
```

---

## 🗄️ Modelo de Dados

### Diagrama ER Simplificado

```
┌─────────────┐
│   Usuario   │
│─────────────│
│ cod_usuario │──┐
│ email       │  │
│ senha       │  │
│ perfil      │  │
│ ...         │  │
└─────────────┘  │
                 │
    ┌────────────┼────────────┬──────────────┐
    │            │            │              │
┌───▼──────┐ ┌──▼────────┐ ┌─▼───────────┐ ┌▼───────────┐
│  Doador  │ │Colaborador│ │AdmUnidade   │ │  Gestor    │
│──────────│ │───────────│ │─────────────│ │────────────│
│cod_doador│ │cod_colab  │ │cod_adm      │ │cod_gestor  │
│tipo_sang │ │cod_unidade│ │cod_unidade  │ │cod_inst    │
│...       │ │...        │ │...          │ │...         │
└──────────┘ └───────────┘ └─────────────┘ └────────────┘
     │            │              │                │
     │            │              │                │
┌────▼────────────▼──────────────▼────────────────▼──────┐
│                    Unidade_Coleta                       │
│─────────────────────────────────────────────────────────│
│ cod_unidade                                             │
│ nome_unidade                                            │
│ cod_instituicao                                         │
│ ...                                                     │
└────────────┬────────────────────────────────────────────┘
             │
     ┌───────┼───────┐
     │       │       │
┌────▼───┐ ┌─▼──────▼──┐ ┌──────────┐
│Estoque │ │ Agendamento│ │ Doacao   │
│────────│ │────────────│ │──────────│
│cod_est │ │cod_agend   │ │cod_doacao│
│tipo    │ │cod_doador  │ │cod_doador│
│qtd_ml  │ │data_hora   │ │data      │
│...     │ │...         │ │...       │
└────────┘ └────────────┘ └──────────┘
```

### Entidades Principais

| Entidade | Descrição | Relacionamentos |
|----------|-----------|-----------------|
| **Usuario** | Usuário base do sistema | 1:1 com Doador, Colaborador, etc. |
| **Doador** | Pessoa que doa sangue | 1:N com Doacao, Agendamento |
| **Colaborador** | Funcionário da unidade | N:1 com UnidadeColeta |
| **AdmUnidade** | Administrador da unidade | 1:1 com UnidadeColeta |
| **Gestor** | Gestor institucional | 1:1 com Instituicao |
| **UnidadeColeta** | Local de coleta | 1:N com diversos |
| **Doacao** | Registro de doação | N:1 com Doador, Unidade |
| **Estoque** | Controle de sangue | 1:1 com UnidadeColeta |
| **Agendamento** | Agendamento de doação | N:1 com Doador, Unidade |
| **Campanha** | Campanha de doação | N:N com Unidades |

---

## 🔐 Fluxo de Autenticação

### Diagrama de Sequência

```
Cliente          FastAPI       Middleware      Repo          Database
  │                │               │             │               │
  │─POST /login───>│               │             │               │
  │  email+senha   │               │             │               │
  │                │               │             │               │
  │                │─────obter_por_email()──────>│               │
  │                │               │             │───SELECT────> │
  │                │               │             │<──Usuario──── │
  │                │<────Usuario────────────────>│               │
  │                │               │             │               │
  │                │─verificar_senha()           │               │
  │                │     (bcrypt)                │               │
  │                │               │             │               │
  │                │──criar_sessao()──>          │               │
  │                │    (session)   │            │               │
  │                │<───────────────>│            │               │
  │                │               │             │               │
  │<──Redirect─────│               │             │               │
  │  Set-Cookie    │               │             │               │
  │                │               │             │               │
  │─GET /doador───>│               │             │               │
  │  Cookie:sess   │               │             │               │
  │                │               │             │               │
  │                │──verificar────>│             │               │
  │                │   sessão       │             │               │
  │                │<──user_data────│             │               │
  │                │               │             │               │
  │<──HTML─────────│               │             │               │
```

### Implementação

#### 1. Login (POST /login)
```python
# routes/auth_routes.py
@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...)
):
    # 1. Buscar usuário por email
    usuario = usuario_repo.obter_por_email(email)
    
    # 2. Verificar senha
    if not usuario or not verificar_senha(senha, usuario.senha):
        return erro("Email ou senha inválidos")
    
    # 3. Criar sessão
    criar_sessao(request, usuario_dict)
    
    # 4. Redirecionar baseado no perfil
    if usuario.perfil == "doador":
        return RedirectResponse("/doador")
```

#### 2. Middleware de Sessão
```python
# main.py
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=28800,  # 8 horas
    same_site="lax",
    https_only=False  # True em produção
)
```

#### 3. Decorator de Autenticação
```python
# util/auth_decorator.py
def requer_autenticacao(perfis: list = None):
    """
    Decorator que protege rotas exigindo autenticação
    
    Args:
        perfis: Lista de perfis autorizados (None = qualquer autenticado)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Verificar se há sessão
            usuario = request.session.get("usuario")
            
            if not usuario:
                return RedirectResponse("/login")
            
            # Verificar perfil se especificado
            if perfis and usuario.get("perfil") not in perfis:
                return erro("Acesso negado")
            
            # Passar usuário para a função
            return await func(request, *args, usuario_logado=usuario, **kwargs)
        
        return wrapper
    return decorator
```

#### 4. Uso em Rotas
```python
@router.get("/doador")
@requer_autenticacao(["doador"])
async def get_doador_home(request: Request, usuario_logado: dict = None):
    """Apenas doadores autenticados podem acessar"""
    return templates.TemplateResponse(...)
```

---

## 🎨 Padrões de Projeto

### 1. Repository Pattern

**Objetivo:** Abstrair acesso aos dados

```python
# Sem Repository (Ruim)
def criar_doacao(doador_id, unidade_id, tipo):
    conexao = sqlite3.connect('dados.db')
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO doacao ...")
    conexao.commit()
    conexao.close()

# Com Repository (Bom)
def criar_doacao(doador_id, unidade_id, tipo):
    doacao = Doacao(...)
    return doacao_repo.inserir(doacao)
```

### 2. DTO Pattern

**Objetivo:** Validar e transferir dados

```python
# Sem DTO (Ruim)
@router.post("/cadastrar")
def cadastrar(nome: str, email: str, ...):
    # Validações manuais
    if not email or '@' not in email:
        raise ValueError("Email inválido")
    ...

# Com DTO (Bom)
@router.post("/cadastrar")
def cadastrar(dados: CriarUsuarioDTO):
    # Validação automática pelo Pydantic
    usuario = Usuario(**dados.dict())
    ...
```

### 3. Decorator Pattern

**Objetivo:** Adicionar funcionalidades sem modificar código original

```python
@router.get("/admin")
@requer_autenticacao(["administrador"])
@log_acesso
@cache(ttl=300)
async def admin_dashboard():
    ...
```

### 4. Dependency Injection

**Objetivo:** Facilitar testes e desacoplamento

```python
# Atual (acoplado)
def criar_usuario():
    repo = usuario_repo
    email = email_service
    ...

# Futuro (desacoplado)
def criar_usuario(
    repo: UsuarioRepo = Depends(get_repo),
    email: EmailService = Depends(get_email_service)
):
    ...
```

---

## 📊 Diagramas de Sistema

### Fluxo de Agendamento

```
Doador          Sistema         Repo          Email
  │                │              │             │
  │─1. Acessar────>│              │             │
  │  agendamento   │              │             │
  │                │              │             │
  │                │─2. Listar───>│             │
  │                │   horários   │             │
  │                │<─Horários────│             │
  │                │   disponíveis│             │
  │                │              │             │
  │<─3. Mostrar────│              │             │
  │   calendário   │              │             │
  │                │              │             │
  │─4. Selecionar─>│              │             │
  │   data/hora    │              │             │
  │                │              │             │
  │                │─5. Validar   │             │
  │                │   doador     │             │
  │                │              │             │
  │                │─6. Verificar>│             │
  │                │   conflitos  │             │
  │                │<─OK──────────│             │
  │                │              │             │
  │                │─7. Criar────>│             │
  │                │   agendamento│             │
  │                │<─ID──────────│             │
  │                │              │             │
  │                │─8. Enviar email────────────>│
  │                │   confirmação│             │
  │                │              │             │
  │<─9. Confirmar──│              │             │
  │   na tela      │              │             │
```

### Fluxo de Doação

```
Colaborador    Sistema      Repo       Estoque     Email
     │            │           │           │          │
     │─1. Buscar─>│           │           │          │
     │   doador   │           │           │          │
     │            │─CPF/Nome─>│           │          │
     │            │<─Doador───│           │          │
     │<─Dados─────│           │           │          │
     │            │           │           │          │
     │─2. Triagem>│           │           │          │
     │   (PA, T°) │           │           │          │
     │            │─Validar───│           │          │
     │            │  apto?    │           │          │
     │            │<─OK───────│           │          │
     │            │           │           │          │
     │─3. Coletar>│           │           │          │
     │   sangue   │           │           │          │
     │            │           │           │          │
     │─4. Anexar─>│           │           │          │
     │   exames   │           │           │          │
     │            │─Salvar───>│           │          │
     │            │  doação   │           │          │
     │            │<─ID───────│           │          │
     │            │           │           │          │
     │            │─Atualizar─────────────>│          │
     │            │  estoque  │           │          │
     │            │<──OK──────────────────│          │
     │            │           │           │          │
     │            │─Notificar doador───────────────> │
     │            │  resultado│           │          │
     │<─Sucesso───│           │           │          │
```

---

## 🤔 Decisões Arquiteturais

### Por que FastAPI?

✅ **Vantagens:**
- Performance comparável a Node.js e Go
- Type hints nativos (Python 3.9+)
- Documentação automática (OpenAPI/Swagger)
- Async/await para operações I/O
- Validação automática com Pydantic

### Por que SQLite?

✅ **Vantagens:**
- Zero configuração
- Serverless (arquivo único)
- Ideal para MVP e projetos pequenos/médios
- Suporta até ~140TB de dados
- ACID compliant

⚠️ **Limitações:**
- Sem concorrência de escrita eficiente
- Sem replicação nativa

**Migração futura:** PostgreSQL ou MySQL para produção em larga escala

### Por que Repository Pattern?

✅ **Benefícios:**
- Testabilidade (mock facilmente)
- Centralização de queries
- Troca de banco transparente
- Reutilização de código

### Por que não ORM?

🤔 **Decisão consciente:**
- SQLite é simples o suficiente
- Queries SQL puras são mais transparentes
- Evita overhead de ORM para projeto deste porte

**Futuro:** Considerar SQLAlchemy se o projeto crescer

---

## 🚀 Próximas Evoluções Arquiteturais

### Versão 2.0

1. **Microserviços**
   - Separar autenticação em serviço próprio
   - API Gateway (Kong/Traefik)
   - Message Queue (RabbitMQ/Redis)

2. **CQRS** (Command Query Responsibility Segregation)
   - Separar leitura de escrita
   - Event Sourcing para auditoria

3. **Cache Distribuído**
   - Redis para sessões e cache
   - Invalidação inteligente

4. **Observabilidade**
   - Logs estruturados (ELK Stack)
   - Métricas (Prometheus + Grafana)
   - Tracing (Jaeger/OpenTelemetry)

---

## 📚 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [12 Factor App](https://12factor.net/)

---

<div align="center">

**Arquitetura desenvolvida pela equipe Hemotec**

</div>
