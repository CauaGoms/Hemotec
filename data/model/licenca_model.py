from dataclasses import dataclass


@dataclass
class Licenca:
    cod_licenca: int
    cod_assinatura: int
    status: int