from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Gestor:
    cod_gestor: int
    cod_usuario: int
    nome: str
    email: str
    senha: str
    cpf: str
    data_nascimento: date
    status: bool
    data_cadastro: date
    rua_usuario: str
    bairro_usuario: str
    cidade_usuario: int
    cep_usuario: str
    telefone: str
    genero: str = ''
    perfil: str = 'gestor'
    foto: Optional[str] = None
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    estado_usuario: Optional[str] = None
    cod_instituicao: int = 0
    instituicao: str = ""