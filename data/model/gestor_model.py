from dataclasses import dataclass
from usuario_model import Usuario

@dataclass
class Gestor(Usuario):
    cod_gestor: int
    cnpj: str
    instituicao: str