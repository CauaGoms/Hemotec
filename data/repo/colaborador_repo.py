from typing import Optional
from data.model.colaborador_model import Colaborador
from data.sql.colaborador_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(colaborador: Colaborador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            colaborador.cod_colaborador,
            colaborador.cod_agendamento,
            colaborador.funcao,
            colaborador.status))
        return cursor.lastrowid
    

def obter_todos() -> list[Colaborador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        colaborador = [
            Colaborador(
                cod_colaborador=row["cod_colaborador"],
                cod_agendamento=row["cod_agendamento"],
                funcao=row["funcao"])  
                for row in rows]
        return colaborador
    
def obter_por_id(cod_colaborador: int) -> Optional[Colaborador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_colaborador,))
        row = cursor.fetchone()
        if row:
            return Colaborador(
                cod_colaborador=row["cod_colaborador"],
                cod_agendamento=row["cod_agendamento"],
                funcao=row["funcao"]
            )
        return None
    
def update(colaborador: Colaborador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                colaborador.cod_colaborador,
                colaborador.cod_agendamento,
                colaborador.funcao
            ),
        )
        return cursor.rowcount > 0

def delete(cod_colaborador: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_colaborador,))
        return cursor.rowcount > 0