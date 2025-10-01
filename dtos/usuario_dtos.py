from pydantic import EmailStr, Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_cpf, validar_telefone
)

class CriarUsuarioDTO(BaseDTO):
    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nome completo do usuário"
    )
    cpf: str = Field(
        ...,
        description="CPF válido do usuário"
    )
    data_nascimento: str = Field(
        ...,
        description="Data de nascimento no formato AAAA-MM-DD"
    )
    email: EmailStr = Field(
        ...,
        description="E-mail válido do usuário"
    )
    telefone: str = Field(
        ...,
        min_length=10,
        description="Telefone com DDD"
    )
    cep_usuario: str = Field(
        ...,
        min_length=8,
        max_length=10,
        description="CEP do usuário"
    )
    rua_usuario: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Rua/Logradouro do usuário"
    )
    bairro_usuario: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Bairro do usuário"
    )
    cidade_usuario: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Cidade do usuário"
    )
    estado_usuario: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Estado (UF) do usuário"
    )
    senha: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Senha do usuário"
    )
    

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Nome"
        )
        return validador(v)

    @field_validator('cpf')
    @classmethod
    def validar_cpf_campo(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf(valor),
            "CPF"
        )
        return validador(v)

    @field_validator('telefone')
    @classmethod
    def validar_telefone_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone"
        )
        return validador(v)

    @field_validator('cep_usuario')
    @classmethod
    def validar_cep(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=8, max_chars=10
            ),
            "CEP"
        )
        return validador(v)

    @field_validator('rua_usuario')
    @classmethod
    def validar_rua(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=200
            ),
            "Rua"
        )
        return validador(v)

    @field_validator('bairro_usuario')
    @classmethod
    def validar_bairro(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Bairro"
        )
        return validador(v)

    @field_validator('cidade_usuario')
    @classmethod
    def validar_cidade(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Cidade"
        )
        return validador(v)

    @field_validator('estado_usuario')
    @classmethod
    def validar_estado(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=2
            ),
            "Estado"
        )
        return validador(v.upper())  # Garante que o estado seja sempre maiúsculo

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=6, max_chars=100
            ),
            "Senha"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "João Silva",
            "cpf": "123.456.789-01",
            "data_nascimento": "1990-05-15",
            "email": "joao.silva@email.com",
            "telefone": "(11) 99999-9999",
            "cep_usuario": "01234-567",
            "rua_usuario": "Rua das Flores, 123",
            "bairro_usuario": "Centro",
            "cidade_usuario": "São Paulo",
            "estado_usuario": "SP",
            "senha": "minhasenha123"
        }
        exemplo.update(overrides)
        return exemplo


# class AtualizarUsuarioDTO(BaseDTO):
#     nome: Optional[str] = Field(
#         None,
#         min_length=2,
#         max_length=100,
#         description="Nome completo"
#     )
#     telefone: Optional[str] = Field(
#         None,
#         description="Telefone"
#     )

#     @field_validator('nome')
#     @classmethod
#     def validar_nome(cls, v: Optional[str]) -> Optional[str]:
#         if not v:
#             return v
#         validador = cls.validar_campo_wrapper(
#             lambda valor, campo: validar_texto_obrigatorio(
#                 valor, campo, min_chars=2, max_chars=100
#             ),
#             "Nome"
#         )
#         return validador(v)

#     @field_validator('telefone')
#     @classmethod
#     def validar_telefone_campo(cls, v: Optional[str]) -> Optional[str]:
#         if not v:
#             return v
#         validador = cls.validar_campo_wrapper(
#             lambda valor, campo: validar_telefone(valor),
#             "Telefone"
#         )
#         return validador(v)


# Configurar exemplos JSON nos model_config
CriarUsuarioDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarUsuarioDTO.criar_exemplo_json()
    }
})