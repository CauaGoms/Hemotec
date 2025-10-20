from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Agendamento:
    cod_agendamento: int
    cod_usuario: int  # Alterado de cod_doador para cod_usuario
    data_hora: Optional[datetime]
    status: int
    tipo_agendamento: str
    local_agendamento: int
    cod_colaborador: Optional[int] = None
    