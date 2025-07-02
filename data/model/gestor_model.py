from dataclasses import dataclass
from data.model.usuario_model import Usuario

@dataclass
class Gestor(Usuario):
    cod_gestor: int
    cod_instituicao: int
    instituicao: str