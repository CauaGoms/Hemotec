from dataclasses import dataclass

@dataclass
class Adm_unidade:
    cod_adm: int
    cod_unidade: int
    permissao_envio_campanha: bool
    permissao_envio_notificacao: bool