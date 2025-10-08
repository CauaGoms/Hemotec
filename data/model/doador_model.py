from dataclasses import dataclass

@dataclass
class Doador:
    cod_doador: int
    tipo_sanguineo: str
    fator_rh: str
    elegivel: str
    altura: float
    peso: float
    profissao: str
    contato_emergencia: str
    telefone_emergencia: str