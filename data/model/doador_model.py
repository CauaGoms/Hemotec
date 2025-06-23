from dataclasses import dataclass
from usuario_model import Usuario


@dataclass
class Doador(Usuario):
    cod_doador: int
    cod_doacao: int
    cod_agendamento: int
    tipo_sanguineo: str
    fator_rh: str
    elegivel: str