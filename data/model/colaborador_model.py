from dataclasses import dataclass


@dataclass
class Colaborador:
    cod_colaborador: int
    cod_agendamento: int
    funcao: str