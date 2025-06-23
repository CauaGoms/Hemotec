from typing import Optional
from data.model.cidade_model import Cidade
from data.sql.cidade_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(cidade: Cidade) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            cidade.nome_cidade, 
            cidade.sigla_estado))
        return cursor.lastrowid
    

def obter_todos() -> list[Cidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        cidade = [
            Cidade(
                cod_cidade=row["cod_cidade"],
                nome_cidade=row["nome_cidade"],
                sigla_estado=row["sigla_estado"])  
                for row in rows]
        return cidade
    
def obter_por_id(cod_cidade: int) -> Optional[Cidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_cidade,))
        row = cursor.fetchone()
        if row:
            return Cidade(
                cod_cidade=row["cod_cidade"],
                nome_cidade=row["cod_campanha"],
                sigla_estado=row["sigla_estado"]
            )
        return None
    
def update(cidade: Cidade) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                cidade.cod_cidade,
                cidade.nome_cidade,
                cidade.sigla_estado
            ),
        )
        return cursor.rowcount > 0

def delete(cod_cidade: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_cidade,))
        return cursor.rowcount > 0