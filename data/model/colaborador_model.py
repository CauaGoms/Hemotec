from dataclasses import dataclass
from data.model.usuario_model import Usuario


@dataclass
class Colaborador:
    cod_colaborador: int
    funcao: str