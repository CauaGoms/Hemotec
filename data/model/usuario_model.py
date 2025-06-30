from dataclasses import dataclass
from datetime import datetime

@dataclass
class Usuario:
    cod_usuario: int
    nome: str
    email: str
    senha: str
    cpf: str
    data_nascimento: datetime
    status: bool
    data_cadastro: datetime
    rua_usuario: str
    bairro_usuario: str
    cidade_usuario: int
    cep_usuario: str
    telefone: str
