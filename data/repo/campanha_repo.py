from typing import Optional
from data.model.campanha_model import Campanha
from data.sql.campanha_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(campanha: Campanha) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            campanha.titulo, 
            campanha.descricao, 
            campanha.data_inicio, 
            campanha.data_fim,
            campanha.status))
        return cursor.lastrowid
    

def obter_todos() -> list[Campanha]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        campanha = [
            Campanha(
                cod_campanha=row["cod_campanha"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                status=row["status"])  
                for row in rows]
        return campanha
    
def obter_por_id(cod_campanha: int) -> Optional[Campanha]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_campanha,))
        row = cursor.fetchone()
        if row:
            return Campanha(
                cod_campanha=row["cod_campanha"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                status=row["status"]
            )
        return None
    
def update(campanha: Campanha) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                campanha.cod_campanha,
                campanha.titulo,
                campanha.descricao,
                campanha.data_inicio,
                campanha.data_fim,
                campanha.status
            ),
        )
        return cursor.rowcount > 0

def delete(cod_campanha: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_campanha,))
        return cursor.rowcount > 0