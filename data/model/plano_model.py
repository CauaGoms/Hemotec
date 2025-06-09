from dataclasses import dataclass


@dataclass
class Plano:
    cod_plano: int
    cod_assinatura: int
    qtd_licenca: int
    nome: str
    valor: float
    validade: int
    