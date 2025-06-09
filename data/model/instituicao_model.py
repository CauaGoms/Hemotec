from dataclasses import dataclass


@dataclass
class Instituicao:
    cnpj: str
    cod_gestor: int
    cod_assinatura: int
    nome: str
    email: str
    rua_instituicao: str
    bairro_instituicao: str
    cidade_instituicao: int
    cep_instituicao: str
    