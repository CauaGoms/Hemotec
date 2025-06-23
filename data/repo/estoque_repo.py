from typing import Optional
from data.model.estoque_model import Estoque
from data.sql.estoque_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(estoque: Estoque) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            estoque.cod_estoque, 
            estoque.cod_unidade, 
            estoque.tipo_sanguineo, 
            estoque.fator_rh, 
            estoque.quantidade,
            estoque.data_atualizacao))
        return cursor.lastrowid
    

def obter_todos() -> list[Estoque]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        estoque = [
            Estoque(
                cod_estoque=row["cod_estoque"],
                cod_unidade=row["cod_unidade"],
                tipo_sanguineo=row["tipo_sanguineo"],
                fator_rh=row["fator_rh"],
                quantidade=row["quantidade"],
                data_atualizacao=row["data_atualizacao"])
                for row in rows]
        return estoque
    
def obter_por_id(cod_estoque: int) -> Optional[Estoque]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_estoque,))
        row = cursor.fetchone()
        if row:
            return Estoque(
                cod_estoque=row["cod_estoque"],
                cod_unidade=row["cod_unidade"],
                tipo_sanguineo=row["tipo_sanguineo"],
                fator_rh=row["fator_rh"],
                quantidade=row["quantidade"],
                data_atualizacao=row["data_atualizacao"]
            )
        return None
    
def update(estoque: Estoque) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                estoque.cod_estoque,
                estoque.cod_unidade,
                estoque.tipo_sanguineo,
                estoque.fator_rh,
                estoque.quantidade,
                estoque.data_atualizacao
            ),
        )
        return cursor.rowcount > 0

def delete(cod_estoque: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_estoque,))
        return cursor.rowcount > 0