from dataclasses import dataclass
from datetime import datetime


@dataclass
class Prontuario:
    cod_prontuario: int
    cod_doacao: int
    data_criacao: datetime
    data_atualizacao: datetime
    jejum: bool
    diabetes: bool
    hipertensao: bool
    cardiopatia: bool
    cancer: bool
    hepatite: bool
    outros: bool
    detalhes_outros: str
    sintomas_gripais: bool
    medicamentos: bool
    detalhes_medicamentos: str
    fumante: bool
    alcool: bool
    droga: bool
    ist: bool
    atividade: bool
    sono: bool
    tatuagem_e_outros: bool
    
    