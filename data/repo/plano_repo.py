from typing import Optional
from data.model.plano_model import Plano
from data.sql.plano_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(plano: Plano) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            plano.cod_plano,
            plano.cod_assinatura,
            plano.qtd_licenca,
            plano.nome,
            plano.valor,
            plano.validade
            ))
        return cursor.lastrowid
    

def obter_todos() -> list[Plano]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        plano = [
            Plano(
                cod_plano=row["cod_plano"],
                cod_assinatura=row["cod_assinatura"],
                qtd_licenca=row["qtd_licenca"],
                nome=row["nome"],
                valor=row["valor"],
                validade=row["validade"]) 
                for row in rows]
        return plano
    
def obter_por_id(cod_plano: int) -> Optional[Plano]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_plano,))
        row = cursor.fetchone()
        if row:
            return Plano(
                cod_plano=row["cod_plano"],
                cod_assinatura=row["cod_assinatura"],
                qtd_licenca=row["qtd_licenca"],
                nome=row["nome"],
                valor=row["valor"],
                validade=row["validade"]
                )
        return None
    
def update(plano: Plano) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                plano.cod_assinatura,
                plano.qtd_licenca,
                plano.nome,
                plano.valor,
                plano.validade,
                plano.cod_plano
            ),
        )
        return cursor.rowcount > 0

def delete(cod_plano: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_plano,))
        return cursor.rowcount > 0