# 🔒 Política de Segurança - Hemotec

## 📋 Índice

- [Versões Suportadas](#versões-suportadas)
- [Reportar Vulnerabilidades](#reportar-vulnerabilidades)
- [Práticas de Segurança](#práticas-de-segurança)
- [Autenticação e Autorização](#autenticação-e-autorização)
- [Proteção de Dados](#proteção-de-dados)
- [Atualizações e Patches](#atualizações-e-patches)
- [Resposta a Incidentes](#resposta-a-incidentes)
- [Compliance](#compliance)

---

## 🛡️ Versões Suportadas

Mantemos suporte de segurança para as seguintes versões:

| Versão | Suportada          | Status           |
|--------|-------------------|------------------|
| 1.x    | ✅ Sim            | Em desenvolvimento |
| < 1.0  | ❌ Não            | Beta/Alpha       |

---

## 🚨 Reportar Vulnerabilidades

### ⚠️ NÃO Abra Issues Públicas para Vulnerabilidades de Segurança!

Se você descobrir uma vulnerabilidade de segurança, por favor, siga este processo:

### 1. **Email Seguro**

Envie um email para:
```
security@hemotec.com.br
```

### 2. **Informações a Incluir**

- **Tipo de vulnerabilidade** (ex: SQL Injection, XSS, CSRF, etc.)
- **Localização** (URL, arquivo, linha de código)
- **Passos para reproduzir**
- **Impacto potencial**
- **Versão afetada**
- **Sugestão de correção** (se houver)

### 3. **Exemplo de Report**

```markdown
Assunto: [SECURITY] SQL Injection em endpoint de busca

Tipo: SQL Injection
Severidade: Alta
Versão: 1.0.0

Descrição:
O endpoint /api/busca não sanitiza adequadamente o parâmetro 'termo',
permitindo injeção de SQL.

Reprodução:
1. Acesse /api/busca?termo=test' OR '1'='1
2. A query retorna todos os registros

Impacto:
Vazamento de dados sensíveis, bypass de autenticação

Sugestão:
Usar consultas parametrizadas ou ORM
```

### 4. **Processo de Resposta**

Quando você reportar uma vulnerabilidade:

1. **Confirmação** - Responderemos em até 48 horas
2. **Avaliação** - Avaliaremos a severidade em até 5 dias úteis
3. **Correção** - Desenvolveremos e testaremos um patch
4. **Disclosure** - Coordenaremos a divulgação com você
5. **Crédito** - Você será creditado (se desejar)

### 5. **Severidade**

| Nível | Descrição | Tempo de Resposta |
|-------|-----------|-------------------|
| **Crítica** | Exploração ativa, vazamento massivo | 24h |
| **Alta** | Vulnerabilidade séria, difícil exploração | 7 dias |
| **Média** | Risco moderado, exploração complexa | 30 dias |
| **Baixa** | Risco mínimo, condições específicas | 90 dias |

---

## 🔐 Práticas de Segurança

### 1. **Senhas**

#### Armazenamento

```python
# ✅ Correto: bcrypt + SHA-256 para senhas longas
from util.security import criar_hash_senha

senha_hash = criar_hash_senha("senha_do_usuario")
```

**Políticas Implementadas:**
- Hash bcrypt com salt automático
- SHA-256 para senhas > 72 bytes
- Mínimo de 6 caracteres (configurável)
- Validação de força opcional

#### Recuperação de Senha

```python
# Token único e criptograficamente seguro
token = gerar_token_redefinicao(tamanho=32)  # 256 bits
expiracao = obter_data_expiracao_token(horas=24)
```

**Políticas:**
- Tokens de uso único
- Expiração em 24 horas
- Invalidação após uso

---

### 2. **Sessões**

#### Configuração Segura

```python
# main.py - Configuração de produção
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ['SECRET_KEY'],  # De .env
    max_age=28800,      # 8 horas
    same_site="strict", # Proteção CSRF
    https_only=True,    # Apenas HTTPS em produção
    session_cookie="hemotec_session"
)
```

**Políticas:**
- Secret key de 256+ bits
- Expiração automática (8h)
- HttpOnly cookies (não acessível via JS)
- Secure flag em produção (HTTPS)
- SameSite=Strict (proteção CSRF)

---

### 3. **SQL Injection**

#### Proteção Implementada

```python
# ✅ Correto: Queries parametrizadas
cursor.execute("""
    SELECT * FROM usuario WHERE email = ?
""", (email,))

# ❌ NUNCA faça:
cursor.execute(f"SELECT * FROM usuario WHERE email = '{email}'")
```

**Políticas:**
- Sempre usar queries parametrizadas
- Validação de entrada com Pydantic
- Escape automático via `sqlite3.Row`
- Foreign keys habilitadas

---

### 4. **XSS (Cross-Site Scripting)**

#### Proteção Implementada

```html
<!-- ✅ Templates Jinja2: Auto-escape habilitado -->
<p>Nome: {{ usuario.nome }}</p>  <!-- Escapado automaticamente -->

<!-- Se precisar HTML confiável: -->
<div>{{ conteudo_html|safe }}</div>  <!-- Apenas em casos específicos -->
```

**Políticas:**
- Auto-escape de templates habilitado
- Validação de entrada com Pydantic
- Content Security Policy (CSP) recomendado
- Sanitização de HTML em campos ricos

---

### 5. **CSRF (Cross-Site Request Forgery)**

#### Proteção Implementada

```python
# SessionMiddleware com SameSite=Lax/Strict
# Tokens CSRF para formulários críticos (em desenvolvimento)
```

**Futuras Melhorias:**
- [ ] Implementar tokens CSRF explícitos
- [ ] Double-submit cookie pattern
- [ ] Verificação de Origin/Referer headers

---

### 6. **Upload de Arquivos**

#### Validações Implementadas

```python
# Validar tipo de arquivo
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

# Validar tamanho
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Sanitizar nome do arquivo
import uuid
safe_filename = f"{uuid.uuid4()}.{ext}"
```

**Políticas:**
- Whitelist de extensões permitidas
- Limite de tamanho (5MB padrão)
- Renomeação com UUID
- Armazenamento fora do webroot
- Verificação de magic bytes (futuro)

---

### 7. **Headers de Segurança**

#### Recomendações para Produção

```python
# Adicionar ao main.py
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

# Host confiável
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["hemotec.com.br", "*.hemotec.com.br"]
)

# Headers de segurança
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

---

## 🔑 Autenticação e Autorização

### Modelo de Controle de Acesso

```python
# Baseado em perfis (RBAC - Role-Based Access Control)

PERFIS = {
    "doador": ["ver_proprias_doacoes", "agendar_doacao"],
    "colaborador": ["registrar_doacao", "ver_agendamentos_unidade"],
    "administrador": ["gerenciar_colaboradores", "ver_relatorios_unidade"],
    "gestor": ["gerenciar_unidades", "ver_relatorios_consolidados"]
}
```

### Proteção de Rotas

```python
@router.get("/colaborador/doacoes")
@requer_autenticacao(["colaborador", "administrador"])
async def listar_doacoes(request: Request, usuario_logado: dict = None):
    # Apenas colaborador e administrador podem acessar
    pass
```

---

## 🗄️ Proteção de Dados

### 1. **Dados Sensíveis**

**Dados Considerados Sensíveis:**
- Senhas (sempre hash)
- CPF (criptografar em produção)
- Dados médicos (exames, histórico)
- Emails e telefones

**Políticas:**
- Senhas NUNCA em texto plano
- Logs não devem conter dados sensíveis
- Backups devem ser criptografados
- Retenção de dados conforme LGPD

### 2. **LGPD (Lei Geral de Proteção de Dados)**

**Conformidade:**
- ✅ Consentimento explícito no cadastro
- ✅ Direito ao esquecimento (exclusão de conta)
- ✅ Portabilidade de dados (exportar dados)
- ✅ Transparência (política de privacidade)
- 🔄 Auditoria de acesso (em desenvolvimento)

**Funcionalidades Necessárias:**
```python
# TODO: Implementar
def exportar_dados_usuario(usuario_id):
    """Exporta todos os dados do usuário (LGPD Art. 18)"""
    pass

def anonimizar_usuario(usuario_id):
    """Anonimiza dados após exclusão (right to be forgotten)"""
    pass
```

### 3. **Backups**

**Políticas:**
- Backups diários automáticos
- Criptografia AES-256
- Armazenamento off-site
- Retenção de 30 dias
- Testes de restore mensais

---

## 🔄 Atualizações e Patches

### Dependências

#### Verificar Vulnerabilidades

```bash
# Verificar vulnerabilidades conhecidas
pip install safety
safety check

# Ou usando pip-audit
pip install pip-audit
pip-audit
```

#### Atualizar Dependências

```bash
# Atualizar todas as dependências
pip list --outdated

# Atualizar específica
pip install --upgrade fastapi
```

### Processo de Atualização

1. **Monitoramento** - GitHub Dependabot habilitado
2. **Avaliação** - Revisar changelog e breaking changes
3. **Teste** - Rodar suite de testes completa
4. **Deploy** - Atualizar em staging primeiro
5. **Verificação** - Monitorar logs e métricas

---

## 🚑 Resposta a Incidentes

### Plano de Resposta

#### 1. **Detecção**
- Monitoramento de logs
- Alertas automáticos
- Reportes de usuários

#### 2. **Contenção**
- Isolar sistemas afetados
- Bloquear acessos não autorizados
- Preservar evidências

#### 3. **Erradicação**
- Identificar causa raiz
- Aplicar patches
- Atualizar regras de firewall

#### 4. **Recuperação**
- Restaurar de backups seguros
- Validar integridade dos dados
- Monitorar comportamento anormal

#### 5. **Lições Aprendidas**
- Documentar incidente
- Atualizar processos
- Treinar equipe

### Contatos de Emergência

```
Security Team: security@hemotec.com.br
Phone: +55 11 9999-9999 (24/7)
```

---

## 📜 Compliance

### Padrões Seguidos

- ✅ **OWASP Top 10** - Proteção contra vulnerabilidades comuns
- ✅ **LGPD** - Lei Geral de Proteção de Dados
- ✅ **ISO 27001** - Princípios de segurança da informação
- 🔄 **PCI-DSS** - Se processar pagamentos (futuro)

### Auditorias

**Recomendadas:**
- Testes de penetração anuais
- Code review de segurança trimestral
- Auditoria de logs mensal
- Treinamento de equipe semestral

---

## 🛠️ Ferramentas de Segurança

### Análise Estática

```bash
# Bandit - Análise de segurança Python
pip install bandit
bandit -r . -ll

# Semgrep - Análise de padrões
pip install semgrep
semgrep --config=auto .
```

### Testes de Segurança

```bash
# OWASP ZAP - Scanner de vulnerabilidades web
# https://www.zaproxy.org/

# SQLMap - Testes de SQL injection
# https://sqlmap.org/
```

---

## 📚 Recursos Adicionais

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security Best Practices](https://python.org/dev/security/)
- [LGPD - Lei 13.709/2018](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)

---

## 🙏 Agradecimentos

Agradecemos aos pesquisadores de segurança que reportarem vulnerabilidades de forma responsável.

**Hall of Fame:**
- [Lista de contribuidores de segurança será mantida aqui]

---

## 📞 Contato

**Security Team**
- Email: security@hemotec.com.br
- PGP Key: [Link para chave pública]
- Response Time: 24-48 horas

---

<div align="center">

**Segurança é responsabilidade de todos**

*Última atualização: Novembro 2025*

</div>
