from dataclasses import dataclass
from datetime import datetime


@dataclass
class Agendamento:
    cod_agendamento: int
    cod_colaborador: int
    cod_doador: int
    data_hora: datetime
    status: int
    observacoes: str
    tipo_agendamento: str
    