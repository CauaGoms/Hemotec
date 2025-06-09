from dataclasses import dataclass


@dataclass
class Doador:
    cod_doador: int
    cod_doacao: int
    cod_agendamento: int
    tipo_sanguineo: str
    fator_rh: str
    elegivel: str