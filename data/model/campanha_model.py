from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class Campanha:
    cod_campanha: int
    titulo: str
    descricao: str
    data_inicio: datetime
    data_fim: datetime
    status: str
    foto: Optional[str] = None