# 🤝 Guia de Contribuição - Hemotec

Obrigado por considerar contribuir com o Hemotec! Este documento fornece diretrizes para contribuir com o projeto.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Posso Contribuir?](#como-posso-contribuir)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Padrões de Código](#padrões-de-código)
- [Padrões de Commit](#padrões-de-commit)
- [Processo de Pull Request](#processo-de-pull-request)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Melhorias](#sugerir-melhorias)

---

## 📜 Código de Conduta

Este projeto e todos os participantes são regidos por nosso Código de Conduta. Ao participar, você concorda em manter um ambiente respeitoso e acolhedor.

### Nossos Compromissos

- Usar linguagem acolhedora e inclusiva
- Respeitar diferentes pontos de vista e experiências
- Aceitar críticas construtivas
- Focar no que é melhor para a comunidade
- Mostrar empatia com outros membros da comunidade

---

## 🚀 Como Posso Contribuir?

### 🐛 Reportar Bugs

Bugs são rastreados como issues do GitHub. Ao criar um issue, forneça:

- **Título claro e descritivo**
- **Passos para reproduzir** o problema
- **Comportamento esperado** vs **comportamento observado**
- **Screenshots** (se aplicável)
- **Ambiente** (SO, versão do Python, etc.)

**Exemplo:**
```markdown
### Descrição
A funcionalidade de agendamento não valida datas passadas

### Passos para Reproduzir
1. Acesse /doador/agendamentos/adicionar
2. Selecione uma data anterior a hoje
3. Clique em "Agendar"

### Comportamento Esperado
Deve exibir mensagem de erro

### Comportamento Observado
Permite agendar com data inválida

### Ambiente
- SO: Windows 11
- Python: 3.11
- Browser: Chrome 120
```

### ✨ Sugerir Melhorias

Melhorias também são rastreadas como issues. Inclua:

- **Descrição clara** da melhoria
- **Justificativa** (por que é útil?)
- **Exemplos** de uso, se possível
- **Alternativas consideradas**

### 💻 Contribuir com Código

1. **Fork** o repositório
2. **Clone** seu fork localmente
3. **Crie uma branch** para sua feature
4. **Implemente** suas mudanças
5. **Teste** suas mudanças
6. **Commit** seguindo nossos padrões
7. **Push** para seu fork
8. Abra um **Pull Request**

---

## 🔄 Processo de Desenvolvimento

### 1. Configurar Ambiente Local

```bash
# Clone seu fork
git clone https://github.com/seu-usuario/Hemotec.git
cd Hemotec

# Adicione o repositório original como upstream
git remote add upstream https://github.com/CauaGoms/Hemotec.git

# Crie ambiente virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt

# Configure o .env
cp .env.example .env
# Edite .env com suas configurações
```

### 2. Criar Branch

Use nomes descritivos para suas branches:

```bash
# Features
git checkout -b feature/nome-da-feature

# Correções
git checkout -b fix/descricao-do-bug

# Documentação
git checkout -b docs/topico-documentado

# Refatoração
git checkout -b refactor/modulo-refatorado
```

### 3. Desenvolvimento

- Escreva código limpo e legível
- Adicione comentários quando necessário
- Siga os padrões de código do projeto
- Escreva testes para novas funcionalidades
- Atualize a documentação conforme necessário

### 4. Testar

```bash
# Executar todos os testes
pytest

# Testar com cobertura
pytest --cov=. --cov-report=html

# Testar arquivo específico
pytest tests/test_usuario_repo.py

# Executar testes verbose
pytest -v
```

### 5. Atualizar com Upstream

```bash
# Buscar mudanças do repositório original
git fetch upstream

# Fazer merge com main
git checkout main
git merge upstream/main

# Rebase sua branch
git checkout sua-branch
git rebase main
```

---

## 📝 Padrões de Código

### Python Style Guide

Seguimos a [PEP 8](https://pep8.org/) com algumas adaptações:

#### Formatação

```python
# ✅ Bom
def calcular_idade_doador(data_nascimento: str) -> int:
    """
    Calcula a idade do doador baseado na data de nascimento.
    
    Args:
        data_nascimento: Data no formato YYYY-MM-DD
        
    Returns:
        Idade em anos completos
    """
    from datetime import datetime
    
    nascimento = datetime.fromisoformat(data_nascimento)
    hoje = datetime.now()
    idade = hoje.year - nascimento.year
    
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1
        
    return idade


# ❌ Ruim
def calc(d):
    from datetime import datetime
    n=datetime.fromisoformat(d)
    h=datetime.now()
    i=h.year-n.year
    if(h.month,h.day)<(n.month,n.day):i-=1
    return i
```

#### Nomenclatura

```python
# Classes: PascalCase
class DoadorModel:
    pass

# Funções e variáveis: snake_case
def obter_doador_por_cpf(cpf: str):
    doador_encontrado = None
    return doador_encontrado

# Constantes: UPPER_CASE
MAX_TENTATIVAS_LOGIN = 3
TEMPO_EXPIRACAO_TOKEN = 3600

# Privados: prefixo _
def _validar_interno():
    pass
```

#### Type Hints

Sempre use type hints em funções:

```python
from typing import Optional, List, Dict

def buscar_doadores(
    cidade: str,
    tipo_sanguineo: Optional[str] = None,
    limite: int = 10
) -> List[Dict[str, any]]:
    """Busca doadores por cidade e tipo sanguíneo."""
    pass
```

#### Docstrings

Use docstrings no formato Google:

```python
def registrar_doacao(
    doador_id: int,
    unidade_id: int,
    tipo_doacao: str
) -> int:
    """
    Registra uma nova doação no sistema.
    
    Args:
        doador_id: ID do doador
        unidade_id: ID da unidade de coleta
        tipo_doacao: Tipo da doação (sangue_total, plasma, plaquetas)
        
    Returns:
        ID da doação registrada
        
    Raises:
        ValueError: Se o tipo de doação for inválido
        DatabaseError: Se houver erro ao salvar no banco
        
    Example:
        >>> registrar_doacao(123, 45, "sangue_total")
        789
    """
    pass
```

### Estrutura de Arquivos

```python
# 1. Imports padrão
import os
import sys
from datetime import datetime

# 2. Imports de terceiros
from fastapi import APIRouter, Request
from pydantic import BaseModel

# 3. Imports locais
from data.repo import usuario_repo
from util.security import criar_hash_senha

# 4. Constantes
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

# 5. Classes e funções
class Usuario(BaseModel):
    pass

def processar_usuario():
    pass
```

### HTML/Templates

```html
<!-- ✅ Bom: Indentação consistente, atributos legíveis -->
<div class="container">
    <form method="post" action="/cadastrar">
        <div class="form-group">
            <label for="nome">Nome Completo:</label>
            <input 
                type="text" 
                id="nome" 
                name="nome" 
                class="form-control"
                required
            >
        </div>
        
        <button type="submit" class="btn btn-primary">
            Cadastrar
        </button>
    </form>
</div>

<!-- ❌ Ruim: Desorganizado, difícil de ler -->
<div class="container"><form method="post" action="/cadastrar"><div class="form-group"><label for="nome">Nome Completo:</label><input type="text" id="nome" name="nome" class="form-control" required></div><button type="submit" class="btn btn-primary">Cadastrar</button></form></div>
```

### JavaScript

```javascript
// ✅ Bom: Código limpo e documentado
/**
 * Valida o formulário de cadastro de doador
 * @param {HTMLFormElement} form - Formulário a ser validado
 * @returns {boolean} True se válido, false caso contrário
 */
function validarFormularioDoador(form) {
    const cpf = form.cpf.value;
    
    if (!validarCPF(cpf)) {
        mostrarErro('CPF inválido');
        return false;
    }
    
    return true;
}

// ❌ Ruim: Sem documentação, variáveis obscuras
function vf(f){let c=f.cpf.value;if(!vCPF(c)){me('CPF inválido');return false}return true}
```

---

## 🎯 Padrões de Commit

Seguimos o [Conventional Commits](https://www.conventionalcommits.org/):

### Formato

```
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé(s) opcional(is)]
```

### Tipos

- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Documentação
- **style**: Formatação (não afeta código)
- **refactor**: Refatoração de código
- **test**: Adicionar ou corrigir testes
- **chore**: Tarefas de manutenção

### Exemplos

```bash
# Feature
git commit -m "feat(doador): adiciona validação de idade mínima"

# Fix
git commit -m "fix(agendamento): corrige validação de datas passadas"

# Documentação
git commit -m "docs(readme): atualiza instruções de instalação"

# Refatoração
git commit -m "refactor(auth): simplifica lógica de autenticação"

# Teste
git commit -m "test(usuario): adiciona testes para cadastro"

# Com corpo e breaking change
git commit -m "feat(api): adiciona endpoint de busca avançada

Implementa busca por múltiplos critérios usando query parameters

BREAKING CHANGE: endpoint /buscar agora requer autenticação"
```

---

## 🔀 Processo de Pull Request

### Checklist antes de abrir PR

- [ ] Código segue os padrões do projeto
- [ ] Testes passam localmente
- [ ] Novos testes foram adicionados (se aplicável)
- [ ] Documentação foi atualizada
- [ ] Commit messages seguem convenção
- [ ] Não há conflitos com a branch main
- [ ] PR tem título descritivo
- [ ] PR tem descrição completa

### Template de Pull Request

```markdown
## Descrição
Breve descrição do que foi implementado/corrigido

## Tipo de Mudança
- [ ] Bug fix (correção de bug)
- [ ] Nova feature (nova funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentação
- [ ] Refatoração
- [ ] Testes

## Como Testar
1. Passo a passo para testar as mudanças
2. Incluir dados de teste necessários
3. Comportamento esperado

## Screenshots (se aplicável)
![descrição](url-da-imagem)

## Checklist
- [ ] Código segue os padrões do projeto
- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Sem conflitos com main

## Issues Relacionadas
Closes #123
Relates to #456
```

### Processo de Review

1. **Automated Checks**: Testes automáticos devem passar
2. **Code Review**: Pelo menos um revisor deve aprovar
3. **Teste Manual**: Revisor testa localmente (se necessário)
4. **Merge**: Maintainer faz merge após aprovação

### Após o Merge

- Sua branch será deletada automaticamente
- Delete seu fork localmente:
  ```bash
  git branch -d feature/sua-feature
  ```
- Atualize sua main:
  ```bash
  git checkout main
  git pull upstream main
  ```

---

## 🐛 Reportar Bugs

### Antes de Reportar

1. **Verifique** se não é um problema local
2. **Busque** issues existentes
3. **Teste** na última versão

### Informações Necessárias

- Versão do sistema
- Sistema operacional
- Versão do Python
- Passos para reproduzir
- Comportamento esperado vs observado
- Logs de erro (se houver)

### Bugs de Segurança

**NÃO** abra issues públicas para vulnerabilidades de segurança!

Envie email para: **security@hemotec.com.br**

Veja [SECURITY.md](SECURITY.md) para mais detalhes.

---

## 💡 Sugerir Melhorias

### Feature Requests

Use o template de issue "Feature Request":

```markdown
## Problema/Necessidade
Descreva qual problema esta feature resolve

## Solução Proposta
Descreva como a feature funcionaria

## Alternativas Consideradas
Outras abordagens que você considerou

## Contexto Adicional
Screenshots, exemplos, etc.
```

### Priorização

Features são priorizadas baseado em:

1. **Impacto**: Quantos usuários serão beneficiados?
2. **Esforço**: Quanto trabalho é necessário?
3. **Alinhamento**: Se alinha com roadmap do projeto?
4. **Comunidade**: Quantos usuários solicitaram?

---

## 🎓 Primeiros Passos

### Bons Primeiros Issues

Procure por labels:

- `good first issue`: Ideal para novos contribuidores
- `help wanted`: Precisamos de ajuda!
- `documentation`: Melhorias na documentação
- `bug`: Bugs confirmados

### Não Sabe Por Onde Começar?

- Melhore a documentação
- Adicione testes
- Corrija typos
- Reporte bugs
- Revise pull requests de outros

---

## 📞 Contato

Dúvidas sobre como contribuir?

- **GitHub Issues**: Para perguntas técnicas
- **Email**: contribuicoes@hemotec.com.br
- **Discord**: [Link do servidor]

---

## 🙏 Agradecimentos

Obrigado por contribuir com o Hemotec! Cada contribuição, grande ou pequena, ajuda a salvar vidas. ❤️

---

<div align="center">

**Desenvolvido com ❤️ pela comunidade Hemotec**

</div>
