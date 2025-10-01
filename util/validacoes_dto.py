import re
from typing import Optional
from decimal import Decimal

class ValidacaoError(ValueError):
    pass

def validar_texto_obrigatorio(
    texto: str,
    campo: str = "Campo",
    min_chars: int = 1,
    max_chars: int = 255
) -> str:
    
    if not texto or not texto.strip():
        raise ValidacaoError(f'{campo} é obrigatório')

    texto_limpo = texto.strip()

    if len(texto_limpo) < min_chars:
        raise ValidacaoError(f'{campo} deve ter pelo menos {min_chars} caracteres')

    if len(texto_limpo) > max_chars:
        raise ValidacaoError(f'{campo} deve ter no máximo {max_chars} caracteres')

    return texto_limpo


def validar_texto_opcional(
    texto: Optional[str],
    max_chars: int = 500
) -> Optional[str]:
    if not texto or not texto.strip():
        return None

    texto_limpo = texto.strip()

    if len(texto_limpo) > max_chars:
        raise ValidacaoError(f'Texto deve ter no máximo {max_chars} caracteres')

    return texto_limpo


def validar_cpf(cpf: Optional[str]) -> Optional[str]:
    if not cpf:
        return None

    # Remover caracteres especiais
    cpf_limpo = re.sub(r'[^0-9]', '', cpf)

    if len(cpf_limpo) != 11:
        raise ValidacaoError('CPF deve ter 11 dígitos')

    # Verificar se todos os dígitos são iguais
    if cpf_limpo == cpf_limpo[0] * 11:
        raise ValidacaoError('CPF inválido')

    # Validar dígito verificador
    def calcular_digito(cpf_parcial):
        soma = sum(int(cpf_parcial[i]) * (len(cpf_parcial) + 1 - i)
                   for i in range(len(cpf_parcial)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    if int(cpf_limpo[9]) != calcular_digito(cpf_limpo[:9]):
        raise ValidacaoError('CPF inválido')

    if int(cpf_limpo[10]) != calcular_digito(cpf_limpo[:10]):
        raise ValidacaoError('CPF inválido')

    return cpf_limpo


def validar_telefone(telefone: str) -> str:
    if not telefone:
        raise ValidacaoError('Telefone é obrigatório')

    # Remover caracteres especiais
    telefone_limpo = re.sub(r'[^0-9]', '', telefone)

    # Telefone deve ter 10 (fixo) ou 11 (celular) dígitos
    if len(telefone_limpo) not in [10, 11]:
        raise ValidacaoError('Telefone deve ter 10 ou 11 dígitos')

    # Validar DDD (11 a 99)
    ddd = int(telefone_limpo[:2])
    if ddd < 11 or ddd > 99:
        raise ValidacaoError('DDD inválido')

    return telefone_limpo


def validar_valor_monetario(
    valor: Optional[Decimal],
    campo: str = "Valor",
    obrigatorio: bool = True,
    min_valor: Optional[Decimal] = None
) -> Optional[Decimal]:
    
    if valor is None:
        if obrigatorio:
            raise ValidacaoError(f'{campo} é obrigatório')
        return None

    if not isinstance(valor, Decimal):
        try:
            valor = Decimal(str(valor))
        except:
            raise ValidacaoError(f'{campo} deve ser um valor numérico válido')

    if min_valor is not None and valor < min_valor:
        raise ValidacaoError(f'{campo} deve ser maior ou igual a {min_valor}')

    return valor


def validar_enum_valor(valor: any, enum_class, campo: str = "Campo"):
    if isinstance(valor, str):
        try:
            return enum_class(valor.upper())
        except ValueError:
            valores_validos = [item.value for item in enum_class]
            raise ValidacaoError(
                f'{campo} deve ser uma das opções: {", ".join(valores_validos)}'
            )

    if valor not in enum_class:
        valores_validos = [item.value for item in enum_class]
        raise ValidacaoError(
            f'{campo} deve ser uma das opções: {", ".join(valores_validos)}'
        )

    return valor

class ValidadorWrapper:
    """
    Classe para facilitar o uso de validadores em field_validators.
    Reduz código repetitivo e padroniza tratamento de erros.
    """

    @staticmethod
    def criar_validador(funcao_validacao, campo_nome: str = None, **kwargs):
        def validador(valor):
            try:
                if campo_nome:
                    return funcao_validacao(valor, campo_nome, **kwargs)
                else:
                    return funcao_validacao(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return validador