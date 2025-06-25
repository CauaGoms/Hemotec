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
    epilepsia: bool
    cancer: bool
    nenhuma: bool
    outros: bool
    outros_detalhe: str
    medicamentos: str
    fumante: str      # "nao", "sim", "parei"
    alcool: str       # "nao", "social", "regular"
    atividade: str    # "nao", "leve", "moderada", "intensa"
    