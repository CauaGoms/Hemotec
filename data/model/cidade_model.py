from dataclasses import dataclass


@dataclass
class Cidade:
    cod_cidade: int
    nome_cidade: str
    sigla_estado: str