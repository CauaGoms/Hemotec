from dataclasses import dataclass
from datetime import datetime


@dataclass
class Assinatura:
    cod_assinatura: int
    cod_instituicao: int
    cod_plano: int
    data_inicio: datetime
    data_fim: datetime
    valor: float
    qtd_licenca: int