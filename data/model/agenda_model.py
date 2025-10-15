from dataclasses import dataclass
from datetime import date, time

@dataclass
class Agenda:
    cod_agenda: int
    cod_unidade: int
    cod_agendamento: int
    data_agenda: date
    hora_agenda: time
    vagas: int
    quantidade_doadores: int
