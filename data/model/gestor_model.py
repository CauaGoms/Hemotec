from dataclasses import dataclass


@dataclass
class Gestor:
    cod_gestor: int
    cnpj: str
    instituicao: str