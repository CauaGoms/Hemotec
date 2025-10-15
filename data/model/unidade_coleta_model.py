from dataclasses import dataclass
from datetime import time

@dataclass
class Unidade_coleta:
    cod_unidade: int
    cod_licenca: int
    cod_horario_funcionamento: int
    nome: str
    email: str
    rua_unidade: str
    bairro_unidade: str
    cidade_unidade: int
    cep_unidade: str
    latitude: float
    longitude: float
    telefone: str