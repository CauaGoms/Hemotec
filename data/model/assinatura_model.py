from dataclasses import dataclass
from datetime import datetime


@dataclass
class Assinatura:
    cod_assinatura: int
    cnpj: str
    cod_plano: int
    data_inicio: datetime
    data_fim: datetime
    valor: float
    qtd_licenca: int