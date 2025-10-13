from dataclasses import dataclass
from datetime import datetime


@dataclass
class Doacao:
    cod_doacao: int
    cod_doador: int
    data_hora: datetime
    quantidade: int
    status: int
    
    