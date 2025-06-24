from dataclasses import dataclass


@dataclass
class Unidade_coleta:
    cod_unidade: int
    cod_adm: int
    cod_licenca: int
    cod_estoque: int
    nome: str
    email: str
    rua_unidade: str
    bairro_unidade: str
    cidade_unidade: int
    cep_unidade: str
    latitude: float
    longitude: float
    telefone: str