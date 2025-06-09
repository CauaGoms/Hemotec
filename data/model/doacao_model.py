from dataclasses import dataclass


@dataclass
class Doacao:
    cod_doacao: int
    cod_doador: int
    cod_exame: int
    data_hora: str
    quantidade: int
    status: int
    