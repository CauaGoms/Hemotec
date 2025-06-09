from dataclasses import dataclass


@dataclass
class Cidade:
    cod_estado: int
    nome_cidade: str
    sigla_estado: str