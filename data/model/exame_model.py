from dataclasses import dataclass
from datetime import datetime


@dataclass
class Exame:
    cod_exame: int
    cod_doacao: int
    data_exame: datetime
    tipo_exame: str
    resultado: str
    arquivo: str
    