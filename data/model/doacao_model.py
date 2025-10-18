from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Doacao:
    cod_doacao: Optional[int]
    cod_doador: int
    cod_agendamento: int
    data_hora: datetime
    quantidade: int
    status: int
    observacoes: str