from dataclasses import dataclass


@dataclass
class Prontuario:
    cod_prontuario: int
    cod_doador: int
    data_criacao: str
    data_atualizacao: str
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
    