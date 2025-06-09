from dataclasses import dataclass


@dataclass
class Exame:
    cod_exame: int
    cod_doacao: int
    data_exame: str
    tipo_exame: str
    resultado: str
    arquivo: str
    