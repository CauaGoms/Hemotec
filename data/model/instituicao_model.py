from dataclasses import dataclass


@dataclass
class Instituicao:
    cod_instituicao: int
    cnpj: str
    nome: str
    email: str
    rua_instituicao: str
    bairro_instituicao: str
    cidade_instituicao: int
    cep_instituicao: str
    telefone: str
    