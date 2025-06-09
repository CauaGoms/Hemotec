from dataclasses import dataclass


@dataclass
class Assinatura:
    cod_assinatura: int
    cnpj: str
    cod_plano: int
    cod_licenca: int
    data_inicio: str
    data_fim: str
    valor: float
    qtd_licenca: int