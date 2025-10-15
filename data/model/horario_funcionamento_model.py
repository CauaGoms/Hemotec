from dataclasses import dataclass
from datetime import date, time

@dataclass
class Horario_funcionamento:
    cod_horario_funcionamento: int
    horario_inicio: time
    horario_fim: time
    intervalo_doacoes: int
    data: date