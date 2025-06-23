from dataclasses import dataclass
from data.model.usuario_model import Usuario

@dataclass
class Adm_unidade(Usuario):
    cod_adm: int
    cod_unidade: int
    cod_notificacao: int
    permissao_envio_campanha: bool
    permissao_envio_notificacao: bool