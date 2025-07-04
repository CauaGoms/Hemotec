from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notificacao:
    cod_notificacao: int
    cod_adm: int
    destino: str
    tipo: str
    mensagem: str
    status: int
    data_envio: datetime