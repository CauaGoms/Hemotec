from dataclasses import dataclass


@dataclass
class Estoque:
    cod_estoque: int
    cod_unidade: int
    tipo_sanguineo: str
    fator_rh: str
    quantidade: int
    data_atualizacao: str
    