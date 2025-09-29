from dataclasses import dataclass
from typing import Optional
from data.model.usuario_model import Usuario


@dataclass
class Doador:
    cod_doador: int
    usuario: Usuario  # Composição: Doador contém um Usuario
    tipo_sanguineo: str
    fator_rh: str
    elegivel: str
    altura: float
    peso: float
    profissao: str
    contato_emergencia: str
    telefone_emergencia: str