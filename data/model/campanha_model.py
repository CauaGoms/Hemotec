from dataclasses import dataclass


@dataclass
class Campanha:
    cod_campanha: int
    titulo: str
    descricao: str
    data_inicio: str
    data_fim: str
    status: str