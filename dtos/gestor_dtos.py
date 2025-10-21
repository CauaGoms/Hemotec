from pydantic import EmailStr, Field, field_validator
from .base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_cpf, validar_telefone
)

class CriarGestorDTO(BaseDTO):
    # Dados pessoais do gestor
    nome_gestor: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nome completo do gestor"
    )
    cpf_gestor: str = Field(
        ...,
        description="CPF válido do gestor"
    )
    data_nascimento_gestor: str = Field(
        ...,
        description="Data de nascimento no formato AAAA-MM-DD"
    )
    email_gestor: EmailStr = Field(
        ...,
        description="E-mail pessoal válido do gestor"
    )
    telefone_gestor: str = Field(
        ...,
        min_length=10,
        description="Telefone do gestor com DDD"
    )
    genero_gestor: str = Field(
        ...,
        description="Gênero do gestor: M, F ou O"
    )
    
    # Endereço do gestor
    cep_gestor: str = Field(
        ...,
        min_length=8,
        max_length=10,
        description="CEP do gestor"
    )
    rua_gestor: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Rua/Logradouro do gestor"
    )
    bairro_gestor: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Bairro do gestor"
    )
    cidade_gestor: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Cidade do gestor"
    )
    estado_gestor: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Estado (UF) do gestor"
    )
    
    # Dados da instituição
    razao_social: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Razão social da instituição"
    )
    cnpj_instituicao: str = Field(
        ...,
        description="CNPJ válido da instituição"
    )
    email_institucional: EmailStr = Field(
        ...,
        description="E-mail institucional válido"
    )
    telefone_instituicao: str = Field(
        ...,
        min_length=10,
        description="Telefone da instituição com DDD"
    )
    
    # Endereço da instituição
    cep_instituicao: str = Field(
        ...,
        min_length=8,
        max_length=10,
        description="CEP da instituição"
    )
    rua_instituicao: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Rua/Logradouro da instituição"
    )
    bairro_instituicao: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Bairro da instituição"
    )
    cidade_instituicao: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Cidade da instituição"
    )
    estado_instituicao: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Estado (UF) da instituição"
    )
    
    # Senha
    senha: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Senha do gestor"
    )

    @field_validator('nome_gestor')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=3, max_chars=100
            ),
            "Nome do gestor"
        )
        return validador(v)

    @field_validator('cpf_gestor')
    @classmethod
    def validar_cpf_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf(valor),
            "CPF do gestor"
        )
        return validador(v)

    @field_validator('telefone_gestor')
    @classmethod
    def validar_telefone_gestor_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone do gestor"
        )
        return validador(v)

    @field_validator('data_nascimento_gestor')
    @classmethod
    def validar_data_nascimento(cls, v: str) -> str:
        import re
        from datetime import datetime
        
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('Data deve estar no formato AAAA-MM-DD')
        
        try:
            data = datetime.strptime(v, '%Y-%m-%d')
            
            if data.date() > datetime.now().date():
                raise ValueError('Data de nascimento não pode ser futura')
            
            if data.year < 1900:
                raise ValueError('Data de nascimento deve ser posterior a 1900')
            
            idade = (datetime.now().date() - data.date()).days // 365
            if idade < 18:
                raise ValueError('Idade mínima para gestor é 18 anos')
                
        except ValueError as e:
            if 'time data' in str(e):
                raise ValueError('Data inválida')
            raise e
        
        return v

    @field_validator('genero_gestor')
    @classmethod
    def validar_genero(cls, v: str) -> str:
        generos_validos = ['M', 'F', 'O']
        if v not in generos_validos:
            raise ValueError(f'Gênero deve ser: M, F ou O')
        return v

    @field_validator('razao_social')
    @classmethod
    def validar_razao_social(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=3, max_chars=200
            ),
            "Razão social"
        )
        return validador(v)

    @field_validator('cnpj_instituicao')
    @classmethod
    def validar_cnpj(cls, v: str) -> str:
        import re
        # Remove formatação
        cnpj = re.sub(r'\D', '', v)
        
        if len(cnpj) != 14:
            raise ValueError('CNPJ deve conter 14 dígitos')
        
        # Validação básica de CNPJ
        if cnpj == cnpj[0] * 14:
            raise ValueError('CNPJ inválido')
        
        return cnpj

    @field_validator('telefone_instituicao')
    @classmethod
    def validar_telefone_instituicao_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone da instituição"
        )
        return validador(v)

    @field_validator('cep_gestor', 'cep_instituicao')
    @classmethod
    def validar_cep(cls, v: str) -> str:
        import re
        cep = re.sub(r'\D', '', v)
        if len(cep) != 8:
            raise ValueError('CEP deve conter 8 dígitos')
        return cep

    @field_validator('rua_gestor', 'rua_instituicao')
    @classmethod
    def validar_rua(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=200
            ),
            "Rua"
        )
        return validador(v)

    @field_validator('bairro_gestor', 'bairro_instituicao')
    @classmethod
    def validar_bairro(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Bairro"
        )
        return validador(v)

    @field_validator('cidade_gestor', 'cidade_instituicao')
    @classmethod
    def validar_cidade(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Cidade"
        )
        return validador(v)

    @field_validator('estado_gestor', 'estado_instituicao')
    @classmethod
    def validar_estado(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=2
            ),
            "Estado"
        )
        return validador(v.upper())

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('Senha deve ter no mínimo 6 caracteres')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve conter pelo menos um número')
        if not any(c.isalpha() for c in v):
            raise ValueError('Senha deve conter pelo menos uma letra')
        return v
