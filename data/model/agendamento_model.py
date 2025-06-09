from dataclasses import dataclass


@dataclass
class Agendamento:
    cod_agendamento: int
    cod_colaborador: int
    cod_doador: int
    data_hora: str
    status: int
    observacoes: str
    tipo_agendamento: str
    