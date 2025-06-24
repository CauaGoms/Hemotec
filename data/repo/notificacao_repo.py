from typing import Optional
from data.model.notificacao_model import Notificacao
from data.sql.notificacao_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(notificacao: Notificacao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            notificacao.cod_notificacao,
            notificacao.cod_adm,
            notificacao.destino,
            notificacao.tipo,
            notificacao.mensagem,
            notificacao.status,
            notificacao.data_envio))
        return cursor.lastrowid
    

def obter_todos() -> list[Notificacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        notificacao = [
            Notificacao(
                cod_notificacao=row["cod_notificacao"],
                cod_adm=row["cod_adm"],
                destino=row["destino"],
                tipo=row["tipo"],
                mensagem=row["mensagem"],
                status=row["status"],
                data_envio=row["data_envio"]) 
                for row in rows]
        return notificacao
    
def obter_por_id(cod_notificacao: int) -> Optional[Notificacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_notificacao,))
        row = cursor.fetchone()
        if row:
            return Notificacao(
                cod_notificacao=row["cod_notificacao"],
                cod_adm=row["cod_adm"],
                destino=row["destino"],
                tipo=row["tipo"],
                mensagem=row["mensagem"],
                status=row["status"],
                data_envio=row["data_envio"]
                ) 
        return None
    
def update(notificacao: Notificacao) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                notificacao.cod_adm,
                notificacao.destino,
                notificacao.tipo,
                notificacao.mensagem,
                notificacao.status,
                notificacao.data_envio,
                notificacao.cod_notificacao
            ),
        )
        return cursor.rowcount > 0

def delete(cod_notificacao: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_notificacao,))
        return cursor.rowcount > 0