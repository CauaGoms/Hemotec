from dataclasses import dataclass


@dataclass
class Notificacao:
    cod_notificacao: int
    cod_adm: int
    destino: str
    tipo: str
    mensagem: str
    status: int
    data_envio: str