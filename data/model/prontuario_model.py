from dataclasses import dataclass
from datetime import datetime


@dataclass
class Prontuario:
    cod_prontuario: int
    cod_doador: int
    data_criacao: datetime
    data_atualizacao: datetime
    diabetes: bool
    hipertensao: bool
    cardiopatia: bool
    cancer: bool
    nenhuma: bool
    outros: bool
    medicamentos: str
    fumante: str
    alcool: str
    atividade: str
    jejum: str
    sono: str
    bebida: str
    sintomas_gripais: str
    tatuagem: str
    termos: str
    alerta: str
    