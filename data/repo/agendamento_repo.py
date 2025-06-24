from typing import Optional
from data.model.agendamento_model import Agendamento
from data.sql.agendamento_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(agendamento: Agendamento) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            agendamento.cod_colaborador,
            agendamento.cod_doador,
            agendamento.data_hora,
            agendamento.status,
            agendamento.observacoes,
            agendamento.tipo_agendamento))
        return cursor.lastrowid
    

def obter_todos() -> list[Agendamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        agendamento = [
            Agendamento(
                cod_agendamento=row["cod_agendamento"],
                cod_colaborador=row["cod_colaborador"],
                cod_doador=row["cod_doador"],
                data_hora=row["data_hora"],
                status=row["status"],
                observacoes=row["observacoes"],
                tipo_agendamento=row["tipo_agendamento"])  
                for row in rows]
        return agendamento
    
def obter_por_id(cod_agendamento: int) -> Optional[Agendamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_agendamento,))
        row = cursor.fetchone()
        if row:
            return Agendamento(
                cod_agendamento=row["cod_agendamento"],
                cod_colaborador=row["cod_colaborador"],
                cod_doador=row["cod_doador"],
                data_hora=row["data_hora"],
                status=row["status"],
                observacoes=row["observacoes"],
                tipo_agendamento=row["tipo_agendamento"]
            )
        return None
    
def update(agendamento: Agendamento) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                agendamento.cod_colaborador,
                agendamento.cod_doador,
                agendamento.data_hora,
                agendamento.cod_agendamento
            ),
        )
        return cursor.rowcount > 0

def delete(cod_agendamento: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_agendamento,))
        return cursor.rowcount > 0