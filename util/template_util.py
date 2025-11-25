from typing import List, Optional, Union
from jinja2 import FileSystemLoader
from fastapi.templating import Jinja2Templates


def criar_templates(diretorio_especifico: Optional[Union[str, List[str]]] = None) -> Jinja2Templates:
    """
    Cria um objeto Jinja2Templates configurado com múltiplos diretórios.
    
    O diretório raiz "templates" é sempre incluído automaticamente para garantir
    acesso aos templates base como base.html.
    
    Args:
        diretorio_especifico: Diretório(s) específico(s) além do raiz.
                             Pode ser uma string única ou lista de strings.
                             Exemplo: "templates/admin/categorias" ou
                                     ["templates/admin", "templates/public"]
    
    Returns:
        Objeto Jinja2Templates configurado com os diretórios especificados
    
    Exemplo de uso:
        # Para um diretório específico
        templates = criar_templates("templates/admin/categorias")
        
        # Para múltiplos diretórios
        templates = criar_templates(["templates/admin", "templates/admin/produtos"])
        
        # Apenas com o diretório raiz
        templates = criar_templates()
    """
    # Sempre incluir o diretório raiz onde estão os templates base
    diretorios = ["templates"]
    
    # Adicionar diretórios específicos se fornecidos
    if diretorio_especifico:
        if isinstance(diretorio_especifico, str):
            # Se for uma string única, adiciona à lista
            diretorios.append(diretorio_especifico)
        elif isinstance(diretorio_especifico, list):
            # Se for uma lista, estende a lista de diretórios
            diretorios.extend(diretorio_especifico)
    
    # Criar o objeto Jinja2Templates com diretório base como "."
    # Isso é necessário para que o FileSystemLoader funcione corretamente
    templates = Jinja2Templates(directory=".")
    
    # Configurar o loader com múltiplos diretórios
    # O FileSystemLoader tentará encontrar templates em ordem nos diretórios listados
    templates.env.loader = FileSystemLoader(diretorios)
    
    # Adicionar filtros personalizados
    templates.env.filters['formatar_cpf'] = formatar_cpf
    templates.env.filters['formatar_telefone'] = formatar_telefone
    templates.env.filters['formatar_cep'] = formatar_cep
    
    return templates


def formatar_cpf(cpf):
    """Formata CPF para o padrão XXX.XXX.XXX-XX"""
    if not cpf:
        return ''
    cpf = ''.join(filter(str.isdigit, str(cpf)))
    if len(cpf) == 11:
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
    return cpf


def formatar_telefone(telefone):
    """Formata telefone para o padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX"""
    if not telefone:
        return ''
    telefone = ''.join(filter(str.isdigit, str(telefone)))
    if len(telefone) == 11:
        return f'({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}'
    elif len(telefone) == 10:
        return f'({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}'
    return telefone


def formatar_cep(cep):
    """Formata CEP para o padrão XXXXX-XXX"""
    if not cep:
        return ''
    cep = ''.join(filter(str.isdigit, str(cep)))
    if len(cep) == 8:
        return f'{cep[:5]}-{cep[5:]}'
    return cep