from pydantic import Field, field_validator, EmailStr
from dtos.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio,
    validar_cpf,
    validar_telefone,
    validar_senha,
    validar_estado_brasileiro,
)

class LoginUsuarioDTO(BaseDTO):
    """DTO para validação de dados de login"""
    email: EmailStr = Field(
        ...,
        description="E-mail válido do usuário"
    )
    senha: str = Field(
        ...,
        description="Senha do usuário"
    )

    @field_validator('email')
    def validar_email_campo(cls, v: str) -> str:
        # EmailStr já faz a validação básica, apenas retornamos
        return v

    @field_validator('senha')
    def validar_senha_campo(cls, v: str) -> str:
        # Para login, validamos se a senha foi fornecida mas sem critérios de complexidade
        # pois a senha já foi validada no cadastro
        if not v or not v.strip():
            raise ValueError('Senha é obrigatória')
        return v

class CriarUsuarioDTO(BaseDTO):
    nome: str = Field(
        ...,
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
        description="Telefone com DDD"
    )
    cep_usuario: str = Field(
        ...,
        description="CEP do usuário"
    )
    rua_usuario: str = Field(
        ...,
        description="Rua/Logradouro do usuário"
    )
    bairro_usuario: str = Field(
        ...,
        description="Bairro do usuário"
    )
    cidade_usuario: str = Field(
        ...,
        description="Cidade do usuário"
    )
    estado_usuario: str = Field(
        ...,
        description="Estado (UF) do usuário"
    )
    senha: str = Field(
        ...,
        description="Senha do usuário"
    )
    confirmar_senha: str = Field(
        ...,
        description="Confirmação da senha do usuário"
    )

    @field_validator("nome")
    def validar_nome(cls, valor):
        # Usar validação de texto obrigatório com limites consistentes ao Field
        validar_texto_obrigatorio(valor, "Nome", min_chars=3, max_chars=100)
        return valor

    @field_validator('cpf')
    def validar_cpf_campo(cls, v: str) -> str:
        # lambda aceita 'campo' opcional para compatibilidade com validar_campo_wrapper
        validador = cls.validar_campo_wrapper(
            lambda valor, campo=None: validar_cpf(valor),
            "CPF"
        )
        return validador(v)

    @field_validator('telefone')
    def validar_telefone_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone"
        )
        return validador(v)

    @field_validator('data_nascimento')
    def validar_data_nascimento(cls, v: str) -> str:
        import re
        from datetime import datetime
        
        # Verifica formato AAAA-MM-DD
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('Data deve estar no formato AAAA-MM-DD')
        
        try:
            data = datetime.strptime(v, '%Y-%m-%d')
            
            # Verifica se não é uma data futura
            if data.date() > datetime.now().date():
                raise ValueError('Data de nascimento não pode ser futura')
            
            # Verifica se não é uma data muito antiga (antes de 1900)
            if data.year < 1900:
                raise ValueError('Data de nascimento deve ser posterior a 1900')
            
            # Verifica idade mínima (16 anos para doação de sangue)
            idade = (datetime.now().date() - data.date()).days // 365
            if idade < 16:
                raise ValueError('Idade mínima para doação é 16 anos')
                
        except ValueError as e:
            if 'time data' in str(e):
                raise ValueError('Data inválida')
            raise e
        
        return v

    @field_validator('email')
    def validar_email_campo(cls, v: str) -> str:
        # EmailStr já faz a validação básica, apenas retornamos
        return v

    @field_validator('cep_usuario')
    def validar_cep(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=8, max_chars=10
            ),
            "CEP"
        )
        return validador(v)

    @field_validator('rua_usuario')
    def validar_rua(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=200
            ),
            "Rua"
        )
        return validador(v)

    @field_validator('bairro_usuario')
    def validar_bairro(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Bairro"
        )
        return validador(v)

    @field_validator('cidade_usuario')
    def validar_cidade(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Cidade"
        )
        return validador(v)

    @field_validator('estado_usuario')
    def validar_estado(cls, v: str) -> str:
        # aceitar 'campo' para manter compatibilidade com o wrapper
        validador = cls.validar_campo_wrapper(
            lambda valor, campo=None: validar_estado_brasileiro(valor), 
            "Estado"
        )
        return validador(v.upper())  # Garante que o estado seja sempre maiúsculo

    @field_validator('senha')
    def validar_senha(cls, v: str) -> str:
        # Usa validação centralizada (lança ValueError contendo a mensagem apropriada)
        validador = cls.validar_campo_wrapper(lambda valor, campo=None: validar_senha(valor), 'Senha')
        return validador(v)
    
    @field_validator('confirmar_senha')
    def senhas_devem_coincidir(cls, v: str, info) -> str:
        if 'senha' in info.data and v != info.data['senha']:
            raise ValueError('As senhas não coincidem')
        return v

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
            ,"confirmar_senha": "minhasenha123"
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