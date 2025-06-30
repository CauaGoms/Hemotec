from dataclasses import dataclass
import datetime


@dataclass
class Campanha:
    cod_campanha: int
    titulo: str
    descricao: str
    data_inicio: datetime
    data_fim: datetime
    status: str