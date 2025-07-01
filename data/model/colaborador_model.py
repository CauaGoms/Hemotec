from dataclasses import dataclass
from data.model.usuario_model import Usuario


@dataclass
class Colaborador(Usuario):
    cod_colaborador: int
    funcao: str