from typing import Optional
from data.model.adm_unidade_model import Adm_unidade
from data.sql.adm_unidade_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(adm_unidade: Adm_unidade) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            adm_unidade.cod_adm, 
            adm_unidade.cod_unidade, 
            adm_unidade.cod_notificacao,
            adm_unidade.permissao_envio_campanha,
            adm_unidade.permissao_envio_notificacao))
        return cursor.lastrowid
    

def obter_todos() -> list[Adm_unidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        adm_unidade = [
            Adm_unidade(
                cod_adm=row["cod_adm"],
                cod_unidade=row["cod_unidade"],
                cod_notificacao=row["cod_notificacao"],
                permissao_envio_campanha=row["permissao_envio_campanha"],
                permissao_envio_notificacao=row["permissao_envio_notificacao"])  
                for row in rows]
        return adm_unidade
    
def obter_por_id(self, cod_adm: int) -> Optional[Adm_unidade]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_adm,))
        row = cursor.fetchone()
        if row:
            return Adm_unidade(
                cod_adm=row["cod_adm"],
                cod_unidade=row["cod_unidade"],
                cod_notificacao=row["papel"],
                permissao_envio_campanha=row["permissao_envio_campanha"],
                permissao_envio_notificacao=row["permissao_envio_notificacao"]
            )
        return None
    
def update(self, adm_unidade: Adm_unidade) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                adm_unidade.cod_adm,
                adm_unidade.cod_unidade,
                adm_unidade.cod_notificacao,
                adm_unidade.permissao_envio_campanha,
                adm_unidade.permissao_envio_notificacao
            ),
        )
        return cursor.rowcount > 0

def delete(self, cod_adm: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_adm,))
        return cursor.rowcount > 0