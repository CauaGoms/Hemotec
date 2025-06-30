from dataclasses import dataclass
from datetime import datetime


@dataclass
class Estoque:
    cod_estoque: int
    cod_unidade: int
    tipo_sanguineo: str
    fator_rh: str
    quantidade: int
    data_atualizacao: datetime
    