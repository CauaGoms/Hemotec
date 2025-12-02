# 📡 Documentação da API - Hemotec

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Autenticação](#autenticação)
- [Endpoints Públicos](#endpoints-públicos)
- [Endpoints do Doador](#endpoints-do-doador)
- [Endpoints do Colaborador](#endpoints-do-colaborador)
- [Endpoints do Administrador](#endpoints-do-administrador)
- [Endpoints do Gestor](#endpoints-do-gestor)
- [APIs REST](#apis-rest)
- [Códigos de Status](#códigos-de-status)
- [Exemplos de Uso](#exemplos-de-uso)

---

## 🎯 Visão Geral

A API do Hemotec é construída sobre FastAPI e fornece endpoints para gerenciamento completo do sistema de doação de sangue.

### Base URL

```
Desenvolvimento: http://127.0.0.1:8000
Produção: https://api.hemotec.com.br
```

### Documentação Interativa

- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

### Formato de Resposta

Todas as respostas seguem o padrão:

```json
{
    "success": true,
    "data": {},
    "message": "Operação realizada com sucesso",
    "errors": []
}
```

---

## 🔐 Autenticação

### Sistema de Sessão

O Hemotec usa **Session-based authentication** com cookies seguros.

#### Login

```http
POST /login
Content-Type: application/x-www-form-urlencoded

email=doador@exemplo.com&senha=senha123
```

**Resposta (Sucesso):**
```http
HTTP/1.1 303 See Other
Location: /doador
Set-Cookie: session=...; Path=/; HttpOnly; SameSite=Lax
```

**Resposta (Erro):**
```html
HTTP/1.1 200 OK
Content-Type: text/html

<!-- Template com mensagem de erro -->
```

#### Logout

```http
GET /usuario/sair
Cookie: session=...
```

**Resposta:**
```http
HTTP/1.1 303 See Other
Location: /
Set-Cookie: session=; Path=/; Max-Age=0
```

### Perfis de Acesso

| Perfil | Descrição | Rotas Base |
|--------|-----------|------------|
| **Doador** | Pessoa que doa sangue | `/doador/*` |
| **Colaborador** | Funcionário da unidade | `/colaborador/*` |
| **Administrador** | Admin de unidade de coleta | `/administrador/*` |
| **Gestor** | Gestor institucional | `/gestor/*` |

---

## 🌐 Endpoints Públicos

### 1. Página Inicial

```http
GET /
```

**Resposta:** Página HTML inicial

---

### 2. Login

```http
GET /login
```

**Resposta:** Formulário de login

```http
POST /login
Content-Type: application/x-www-form-urlencoded

email=usuario@exemplo.com
senha=senha123
redirect=/destino (opcional)
```

---

### 3. Cadastro de Doador

```http
GET /cadastrar
```

**Resposta:** Formulário de cadastro

```http
POST /cadastrar
Content-Type: application/x-www-form-urlencoded

nome=João Silva
cpf=12345678900
data_nascimento=1990-01-01
email=joao@exemplo.com
telefone=11999999999
cep_usuario=12345678
rua_usuario=Rua Exemplo
bairro_usuario=Centro
cidade_usuario=São Paulo
estado_usuario=SP
genero=M
senha=senha123
confirmar_senha=senha123
```

**Resposta (Sucesso):**
```http
HTTP/1.1 303 See Other
Location: /login
```

**Resposta (Erro):**
```html
<!-- Template com erros de validação -->
```

---

### 4. Redefinir Senha

```http
GET /redefinir-senha
```

**Resposta:** Formulário de redefinição

```http
POST /redefinir-senha
Content-Type: application/x-www-form-urlencoded

email=usuario@exemplo.com
```

**Resposta:**
```http
HTTP/1.1 303 See Other
Location: /validar-token
```

---

### 5. Campanhas Públicas

```http
GET /campanhas
```

**Resposta:** Lista de campanhas ativas

**Query Parameters:**
- `cidade` (opcional): Filtrar por cidade
- `estado` (opcional): Filtrar por estado

---

### 6. Sobre

```http
GET /sobre
```

**Resposta:** Página sobre o sistema

---

### 7. Contato

```http
GET /contato
```

**Resposta:** Formulário de contato

```http
POST /contato
Content-Type: application/x-www-form-urlencoded

nome=João
email=joao@exemplo.com
mensagem=Gostaria de informações
```

---

## 🩸 Endpoints do Doador

**Requer:** Autenticação com perfil "doador"

### 1. Dashboard

```http
GET /doador
Cookie: session=...
```

**Resposta:** Página inicial do doador

---

### 2. Agendamentos

#### Listar Agendamentos

```http
GET /doador/agendamentos
Cookie: session=...
```

**Resposta:** Lista de agendamentos do doador

#### Adicionar Agendamento

```http
GET /doador/agendamentos/adicionar
Cookie: session=...
```

**Resposta:** Formulário de agendamento

```http
POST /doador/agendamentos/adicionar
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

unidade_id=1
data=2025-12-01
hora=14:00
tipo_doacao=sangue_total
```

#### Alterar Agendamento

```http
GET /doador/agendamentos/alterar/{agendamento_id}
Cookie: session=...
```

```http
POST /doador/agendamentos/alterar/{agendamento_id}
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

data=2025-12-02
hora=15:00
```

#### Excluir Agendamento

```http
POST /doador/agendamentos/excluir/{agendamento_id}
Cookie: session=...
```

---

### 3. Histórico de Doações

```http
GET /doador/doacoes
Cookie: session=...
```

**Query Parameters:**
- `ano` (opcional): Filtrar por ano

**Resposta:** Lista de doações do doador

---

### 4. Detalhes da Doação

```http
GET /doador/doacoes/{doacao_id}
Cookie: session=...
```

**Resposta:** Detalhes completos da doação

---

### 5. Carteira do Doador

```http
GET /doador/carteira
Cookie: session=...
```

**Resposta:** Carteira digital do doador (PDF ou HTML)

---

### 6. Campanhas

```http
GET /doador/campanhas
Cookie: session=...
```

**Resposta:** Campanhas disponíveis para o doador

```http
GET /doador/campanhas/{campanha_id}
Cookie: session=...
```

**Resposta:** Detalhes da campanha

---

### 7. Notificações

```http
GET /doador/notificacoes
Cookie: session=...
```

**Resposta:** Lista de notificações do doador

---

### 8. Configurações

```http
GET /doador/configuracoes
Cookie: session=...
```

**Resposta:** Página de configurações

---

## 👨‍⚕️ Endpoints do Colaborador

**Requer:** Autenticação com perfil "colaborador"

### 1. Dashboard

```http
GET /colaborador
Cookie: session=...
```

---

### 2. Agendamentos

#### Listar Agendamentos da Unidade

```http
GET /colaborador/agendamentos
Cookie: session=...
```

**Query Parameters:**
- `data` (opcional): Filtrar por data (YYYY-MM-DD)
- `status` (opcional): pendente, confirmado, cancelado

#### Adicionar Agendamento (Agendar para Doador)

```http
POST /colaborador/agendamentos/adicionar
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

doador_cpf=12345678900
data=2025-12-01
hora=14:00
tipo_doacao=sangue_total
```

---

### 3. Doações

#### Listar Doações

```http
GET /colaborador/doacoes
Cookie: session=...
```

**Query Parameters:**
- `data_inicio` (opcional): Data inicial (YYYY-MM-DD)
- `data_fim` (opcional): Data final (YYYY-MM-DD)
- `status` (opcional): triagem, coletada, exame, finalizada

#### Adicionar Doação

```http
GET /colaborador/doacoes/adicionar
Cookie: session=...
```

```http
POST /colaborador/doacoes/adicionar
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

doador_cpf=12345678900
data=2025-11-26
tipo_doacao=sangue_total
volume_ml=450
```

#### Registrar Triagem

```http
GET /colaborador/doacoes/{doacao_id}/triagem
Cookie: session=...
```

```http
POST /colaborador/doacoes/{doacao_id}/triagem
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

pressao_arterial=120x80
temperatura=36.5
peso=70
hemoglobina=14.5
apto=sim
observacoes=Doador apto
```

#### Anexar Resultado de Exame

```http
POST /colaborador/doacoes/{doacao_id}/anexar-resultado
Cookie: session=...
Content-Type: multipart/form-data

arquivo=@resultado.pdf
tipo_exame=hiv,hepatite,sifilis
```

---

### 4. Campanhas

```http
GET /colaborador/campanhas
Cookie: session=...
```

```http
POST /colaborador/campanhas/adicionar
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

titulo=Campanha Novembro
descricao=Doe sangue neste mês
data_inicio=2025-11-01
data_fim=2025-11-30
meta_doacoes=100
```

---

### 5. Disponibilidade de Coleta

```http
GET /colaborador/disponibilidade
Cookie: session=...
```

```http
POST /colaborador/disponibilidade
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

data=2025-12-01
horario_inicio=08:00
horario_fim=17:00
capacidade=20
```

---

## 🏥 Endpoints do Administrador

**Requer:** Autenticação com perfil "administrador"

### 1. Dashboard

```http
GET /administrador
Cookie: session=...
```

---

### 2. Colaboradores

#### Listar Colaboradores

```http
GET /administrador/colaboradores
Cookie: session=...
```

#### Adicionar Colaborador

```http
POST /administrador/colaboradores/adicionar
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

nome=Maria Santos
email=maria@unidade.com
cpf=98765432100
cargo=enfermeira
```

#### Detalhes do Colaborador

```http
GET /administrador/colaboradores/{colaborador_id}
Cookie: session=...
```

#### Alterar Colaborador

```http
POST /administrador/colaboradores/{colaborador_id}/alterar
Cookie: session=...
```

#### Excluir Colaborador

```http
POST /administrador/colaboradores/{colaborador_id}/excluir
Cookie: session=...
```

---

### 3. Campanhas da Unidade

```http
GET /administrador/campanhas
Cookie: session=...
```

```http
POST /administrador/campanhas/adicionar
Cookie: session=...
```

---

### 4. Relatórios

#### Relatórios Gerais

```http
GET /administrador/relatorios
Cookie: session=...
```

#### Relatório por Tipo Sanguíneo

```http
GET /administrador/relatorios/tipo-sanguineo
Cookie: session=...
```

**Query Parameters:**
- `tipo` (opcional): A, B, AB, O
- `fator_rh` (opcional): +, -

#### Relatório por Período

```http
GET /administrador/relatorios/periodo
Cookie: session=...
```

**Query Parameters:**
- `data_inicio`: Data inicial (YYYY-MM-DD)
- `data_fim`: Data final (YYYY-MM-DD)

---

### 5. Notificações

```http
GET /administrador/notificacoes
Cookie: session=...
```

---

## 🎯 Endpoints do Gestor

**Requer:** Autenticação com perfil "gestor"

### 1. Dashboard

```http
GET /gestor
Cookie: session=...
```

---

### 2. Unidades de Coleta

#### Listar Unidades

```http
GET /gestor/centro-coleta
Cookie: session=...
```

#### Adicionar Unidade

```http
POST /gestor/centro-coleta/adicionar
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

nome_unidade=Hemocentro Centro
endereco=Rua Central, 123
cidade=São Paulo
estado=SP
telefone=1133334444
```

#### Detalhes da Unidade

```http
GET /gestor/centro-coleta/{unidade_id}
Cookie: session=...
```

#### Alterar Unidade

```http
POST /gestor/centro-coleta/{unidade_id}/alterar
Cookie: session=...
```

#### Excluir Unidade

```http
POST /gestor/centro-coleta/{unidade_id}/excluir
Cookie: session=...
```

---

### 3. Administradores

```http
GET /gestor/administradores
Cookie: session=...
```

```http
POST /gestor/administradores/adicionar
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

nome=Carlos Admin
email=carlos@gestor.com
cpf=11122233344
unidade_id=1
```

---

### 4. Relatórios Consolidados

#### Relatório de Colaboradores

```http
GET /gestor/relatorio/colaboradores
Cookie: session=...
```

**Query Parameters:**
- `unidade_id` (opcional): Filtrar por unidade

#### Relatório de Doadores

```http
GET /gestor/relatorio/doadores
Cookie: session=...
```

**Query Parameters:**
- `periodo` (opcional): mensal, trimestral, anual
- `unidade_id` (opcional): Filtrar por unidade

---

## 🔌 APIs REST

### 1. API de Agenda

#### Obter Horários Disponíveis

```http
GET /api/agenda/horarios-disponiveis
```

**Query Parameters:**
- `unidade_id`: ID da unidade (obrigatório)
- `data`: Data desejada no formato YYYY-MM-DD (obrigatório)

**Resposta:**
```json
{
    "success": true,
    "data": {
        "unidade_id": 1,
        "data": "2025-12-01",
        "horarios": [
            {"hora": "08:00", "disponivel": true, "vagas": 5},
            {"hora": "09:00", "disponivel": true, "vagas": 3},
            {"hora": "10:00", "disponivel": false, "vagas": 0}
        ]
    }
}
```

---

### 2. API de Cidades

#### Buscar Cidades

```http
GET /api/cidades
```

**Query Parameters:**
- `estado`: Sigla do estado (obrigatório)
- `termo` (opcional): Termo de busca

**Resposta:**
```json
{
    "success": true,
    "data": [
        {"cod_cidade": 1, "nome_cidade": "São Paulo", "sigla_estado": "SP"},
        {"cod_cidade": 2, "nome_cidade": "Campinas", "sigla_estado": "SP"}
    ]
}
```

---

### 3. API Pública

#### Informações Gerais

```http
GET /api/public/info
```

**Resposta:**
```json
{
    "success": true,
    "data": {
        "nome": "Hemotec",
        "versao": "1.0.0",
        "unidades_ativas": 15,
        "campanhas_ativas": 8
    }
}
```

---

## 📊 Códigos de Status

| Código | Significado | Uso |
|--------|-------------|-----|
| **200** | OK | Requisição bem-sucedida |
| **303** | See Other | Redirecionamento após POST |
| **400** | Bad Request | Dados inválidos |
| **401** | Unauthorized | Não autenticado |
| **403** | Forbidden | Sem permissão |
| **404** | Not Found | Recurso não encontrado |
| **500** | Internal Server Error | Erro no servidor |

---

## 💡 Exemplos de Uso

### Python (requests)

```python
import requests

# Login
session = requests.Session()
response = session.post(
    'http://127.0.0.1:8000/login',
    data={
        'email': 'doador@exemplo.com',
        'senha': 'senha123'
    }
)

# Acessar área autenticada
response = session.get('http://127.0.0.1:8000/doador/agendamentos')
print(response.text)
```

### JavaScript (fetch)

```javascript
// Login
const formData = new FormData();
formData.append('email', 'doador@exemplo.com');
formData.append('senha', 'senha123');

fetch('http://127.0.0.1:8000/login', {
    method: 'POST',
    body: formData,
    credentials: 'include'  // Importante para cookies
})
.then(response => {
    if (response.redirected) {
        window.location.href = response.url;
    }
});

// Buscar horários disponíveis
fetch('/api/agenda/horarios-disponiveis?unidade_id=1&data=2025-12-01')
    .then(r => r.json())
    .then(data => console.log(data.data.horarios));
```

### cURL

```bash
# Login
curl -c cookies.txt -X POST \
  http://127.0.0.1:8000/login \
  -d "email=doador@exemplo.com&senha=senha123"

# Acessar área autenticada
curl -b cookies.txt \
  http://127.0.0.1:8000/doador/agendamentos

# API REST
curl http://127.0.0.1:8000/api/cidades?estado=SP
```

---

## 🔒 Boas Práticas de Segurança

### 1. Sempre Use HTTPS em Produção

```python
# main.py (produção)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ['SECRET_KEY'],  # De variável de ambiente
    https_only=True,  # Força HTTPS
    same_site="strict"
)
```

### 2. Valide Todas as Entradas

```python
# Use DTOs do Pydantic
@router.post("/cadastrar")
def cadastrar(dados: CriarUsuarioDTO):
    # Validação automática
    pass
```

### 3. Rate Limiting

```python
# Implementar limite de requisições
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
def login():
    pass
```

### 4. Sanitize Outputs

```python
# Escape HTML em templates
{{ usuario.nome|e }}
```

---

## 📞 Suporte

Dúvidas sobre a API?

- **Email:** api@hemotec.com.br
- **Issues:** [GitHub Issues](https://github.com/CauaGoms/Hemotec/issues)
- **Documentação Interativa:** `/docs`

---

<div align="center">

**API desenvolvida pela equipe Hemotec**

</div>
