from dataclasses import dataclass


@dataclass
class Usuario:
    cod_usuario: int
    nome: str
    email: str
    senha: str
    cpf: str
    data_nascimento: str
    status: bool
    data_cadastro: str
    rua_usuario: str
    bairro_usuario: str
    cidade_usuario: int
    cep_usuario: str
