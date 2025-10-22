from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from data.model.usuario_model import Usuario


@dataclass
class Colaborador(Usuario):
    cod_colaborador: int = 0
    funcao: str = ""