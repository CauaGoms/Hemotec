from dataclasses import dataclass
from datetime import datetime


@dataclass
class Agendamento:
    cod_agendamento: int
    cod_colaborador: int
    cod_doador: int
    data_hora: datetime
    status: int
    tipo_agendamento: str
    local_agendamento: int
    