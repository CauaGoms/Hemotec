# Configuração da Verificação de Email

## ✉️ Sobre

A plataforma Hemotec agora requer verificação de email para novos doadores. Antes de acessar a área do doador, o usuário deve confirmar seu email inserindo um código de 6 dígitos enviado via Resend.com.

## 🔧 Configuração do Resend.com

### 1. Criar Conta no Resend

1. Acesse [resend.com](https://resend.com/)
2. Crie uma conta gratuita
3. Verifique seu domínio de envio (ou use o domínio de teste fornecido)

### 2. Obter API Key

1. No dashboard do Resend, vá em **API Keys**
2. Clique em **Create API Key**
3. Dê um nome (ex: "Hemotec Production")
4. Copie a chave gerada (começa com `re_`)

### 3. Configurar no Projeto

Edite o arquivo `util/email_service.py` e atualize:

```python
RESEND_API_KEY = "sua_chave_api_aqui"  # Cole a chave do Resend
SENDER_EMAIL = "seu-email@seudominio.com"  # Email verificado no Resend
SENDER_NAME = "Hemotec"
```

**Importante:** Em produção, use variáveis de ambiente:

```python
import os
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
```

### 4. Instalar Dependência

```bash
pip install resend
```

Ou adicione ao `requirements.txt`:
```
resend>=0.8.0
```

## 📧 Verificar Domínio de Email

Para usar um email personalizado (ex: `noreply@hemotec.com.br`), você precisa:

1. No Resend, vá em **Domains**
2. Clique em **Add Domain**
3. Digite seu domínio (ex: `hemotec.com.br`)
4. Adicione os registros DNS fornecidos (SPF, DKIM, DMARC)
5. Aguarde a verificação (pode levar até 72h)

**Durante testes**, use o email de teste fornecido pelo Resend:
```python
SENDER_EMAIL = "onboarding@resend.dev"
```

## 🚀 Fluxo Implementado

### Cadastro

1. Usuário preenche formulário de cadastro
2. Sistema cria usuário no banco com `email_verificado = 0`
3. Gera código de 6 dígitos aleatório
4. Envia email com código via Resend
5. Armazena código e timestamp no banco
6. Redireciona para `/verificar-email`

### Verificação

1. Usuário insere código de 6 dígitos
2. Sistema valida:
   - Código está correto?
   - Código não expirou? (30 minutos)
3. Se válido:
   - Marca `email_verificado = 1`
   - Limpa código do banco
   - Redireciona para `/login`

### Login

1. Usuário faz login com email/senha
2. Sistema verifica se `email_verificado = 1`
3. Se **não verificado** (apenas para doadores):
   - Gera novo código (se necessário)
   - Envia novo email
   - Redireciona para `/verificar-email`
4. Se **verificado**:
   - Cria sessão
   - Redireciona para área do doador

### Reenviar Código

1. Na tela de verificação, botão "Reenviar Código"
2. Gera novo código
3. Atualiza banco com novo código e timestamp
4. Envia novo email
5. Mostra mensagem de sucesso

## 🗄️ Estrutura do Banco

```sql
-- Campos adicionados na tabela usuario:
email_verificado INTEGER DEFAULT 0
codigo_verificacao TEXT
data_codigo_verificacao TIMESTAMP
```

## 📁 Arquivos Criados/Modificados

### Novos Arquivos

- `util/email_service.py` - Serviço de envio de email com Resend
- `routes/verificar_email_routes.py` - Rotas de verificação
- `templates/publico/publico_verificar_email.html` - Template de verificação
- `migrate_add_email_verification.py` - Migration para adicionar campos

### Arquivos Modificados

- `data/model/usuario_model.py` - Adicionados campos de verificação
- `data/sql/usuario_sql.py` - Atualizados SELECTs com novos campos
- `data/repo/usuario_repo.py` - Novos métodos de verificação
- `routes/auth_routes.py` - Validação no login e envio no cadastro
- `main.py` - Registro da nova rota

## 🧪 Testando Localmente

### Sem Resend (Mock)

Para testar sem enviar emails reais, comente o envio no `auth_routes.py`:

```python
# email_enviado = enviar_email_verificacao(dados.email, dados.nome, codigo)
print(f"CÓDIGO DE TESTE: {codigo}")  # Mostrar no console
```

### Com Resend (Recomendado)

1. Configure a API key
2. Use o email de teste: `onboarding@resend.dev`
3. Faça um cadastro
4. Verifique o email recebido
5. Insira o código de 6 dígitos

## 🔒 Segurança

- ✅ Código expira em 30 minutos
- ✅ Código armazenado apenas no banco (não em cookies)
- ✅ Validação no servidor (não apenas no frontend)
- ✅ Email verificado é obrigatório para doadores
- ✅ Outros perfis (gestor, colaborador) não precisam verificar

## 📊 Logs

Verifique os logs no console do servidor:

```
✓ Email enviado com sucesso para usuario@example.com. ID: abc123
✗ Erro ao enviar email para usuario@example.com: [erro]
```

## 🐛 Troubleshooting

### Email não está sendo enviado

1. Verifique a API key no `email_service.py`
2. Confirme que o domínio está verificado no Resend
3. Verifique os logs do servidor
4. Teste a API key diretamente no Resend Dashboard

### Código sempre inválido

1. Verifique se os campos foram criados no banco:
   ```sql
   PRAGMA table_info(usuario);
   ```
2. Execute a migration novamente se necessário:
   ```bash
   python migrate_add_email_verification.py
   ```

### Sessão expirada

Se aparecer "Sessão expirada", o usuário precisa fazer cadastro novamente. Isso acontece se:
- Cookie de sessão foi apagado
- Servidor foi reiniciado sem sessões persistentes
- Passou muito tempo sem verificar

## 📝 Próximos Passos

- [ ] Adicionar rate limiting (máximo de emails por hora)
- [ ] Template de email personalizado com HTML/CSS
- [ ] Link de verificação por email (alternativa ao código)
- [ ] Histórico de tentativas de verificação
- [ ] Notificação de login em novo dispositivo

## 📞 Suporte

Em caso de dúvidas:
- Documentação Resend: https://resend.com/docs
- Email: suporte@hemotec.com.br
