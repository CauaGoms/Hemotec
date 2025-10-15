"""
Funções utilitárias para formatação de dados
"""
from datetime import datetime, date


def formatar_cpf(cpf: str) -> str:
    """Formata CPF para o padrão XXX.XXX.XXX-XX"""
    if not cpf:
        return ""
    # Remove caracteres não numéricos
    cpf_numeros = ''.join(filter(str.isdigit, cpf))
    if len(cpf_numeros) == 11:
        return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
    return cpf


def formatar_data(data) -> str:
    """Converte data para formato DD/MM/YYYY"""
    if not data:
        return ""
    
    # Se já é um objeto date ou datetime
    if isinstance(data, (datetime, date)):
        return data.strftime('%d/%m/%Y')
    
    # Se é string, tenta converter
    if isinstance(data, str):
        try:
            # Tenta formato YYYY-MM-DD
            data_obj = datetime.strptime(data, '%Y-%m-%d')
            return data_obj.strftime('%d/%m/%Y')
        except ValueError:
            try:
                # Tenta formato DD/MM/YYYY (já está formatado)
                datetime.strptime(data, '%d/%m/%Y')
                return data
            except ValueError:
                return data
    
    return str(data)


def formatar_tipo_sanguineo(tipo: str, fator_rh: str) -> str:
    """Formata tipo sanguíneo para o padrão A+, A-, O+, etc."""
    if not tipo or not fator_rh:
        return "N/A"
    
    # Converter fator RH para símbolo + ou -
    fator_simbolo = ""
    fator_lower = fator_rh.lower()
    
    if "positiv" in fator_lower or fator_lower == "+":
        fator_simbolo = "+"
    elif "negativ" in fator_lower or fator_lower == "-":
        fator_simbolo = "-"
    else:
        # Se não reconhecer, usar o valor original
        fator_simbolo = fator_rh
    
    # Combinar tipo e fator com espaço
    return f"{tipo.upper()}{fator_simbolo}"
