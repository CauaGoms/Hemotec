from dataclasses import dataclass
from data.model.usuario_model import Usuario


@dataclass
class Doador(Usuario):
    cod_doador: int
    cod_doacao: int
    cod_agendamento: int
    tipo_sanguineo: str
    fator_rh: str
    elegivel: str
    altura: float
    peso: float
    profissao: str
    contato_emergencia: str
    telefone_emergencia: str