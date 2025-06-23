from typing import Optional
from data.model.doador_model import Doador
from data.sql.doador_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(doador: Doador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            doador.cod_doador, 
            doador.cod_doacao, 
            doador.cod_agendamento,
            doador.tipo_sanguineo,
            doador.fator_rh,
            doador.elegivel))
        return cursor.lastrowid
    

def obter_todos() -> list[Doador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        doador = [
            Doador(
                cod_doador=row["cod_doador"],
                cod_doacao=row["cod_doacao"],
                cod_agendamento=row["cod_agendamento"],
                tipo_sanguineo=row["tipo_sanguineo"],
                fator_rh=row["fator_rh"],
                elegivel=row["elegivel"])  
                for row in rows]
        return doador
    
def obter_por_id(cod_doador: int) -> Optional[Doador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_doador,))
        row = cursor.fetchone()
        if row:
            return Doador(
                cod_doador=row["cod_doador"],
                cod_doacao=row["cod_doacao"],
                cod_agendamento=row["cod_agendamento"],
                tipo_sanguineo=row["tipo_sanguineo"],
                fator_rh=row["fator_rh"],
                elegivel=row["elegivel"]
            )
        return None
    
def update(doador: Doador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                doador.cod_doador,
                doador.cod_doacao,
                doador.cod_agendamento,
                doador.tipo_sanguineo,
                doador.fator_rh,
                doador.elegivel
            ),
        )
        return cursor.rowcount > 0

def delete(cod_doador: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_doador,))
        return cursor.rowcount > 0