from dataclasses import dataclass


@dataclass
class Licenca:
    cod_licenca: int
    cod_assinatura: int
    cod_unidade: int
    status: int