from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Adm_unidade:
    cod_adm: int
    nome: str
    email: str
    senha: str
    cpf: str
    data_nascimento: datetime
    status: bool
    data_cadastro: datetime
    rua_usuario: str
    bairro_usuario: str
    cidade_usuario: int
    cep_usuario: str
    telefone: str
    cod_unidade: int
    permissao_envio_campanha: bool
    permissao_envio_notificacao: bool
    genero: Optional[str] = None
    perfil: str = 'adm_unidade'
    foto: Optional[str] = None