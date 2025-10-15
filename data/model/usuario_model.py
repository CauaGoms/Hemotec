from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Usuario:
    cod_usuario: int
    nome: str
    email: str
    senha: str # Optional[str] = None
    cpf: str
    data_nascimento: datetime
    status: bool
    rua_usuario: str
    bairro_usuario: str
    cidade_usuario: int
    cep_usuario: str
    telefone: str
    perfil: str = 'doador'
    genero: str
    data_cadastro: Optional[str] = None
    foto: Optional[str] = None
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    estado_usuario: Optional[str] = None
