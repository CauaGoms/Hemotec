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
    data_cadastro: datetime
    rua_usuario: str
    bairro_usuario: str
    cidade_usuario: int
    cep_usuario: str
    telefone: str
