from typing import Optional
from data.model.exame_model import Exame
from data.sql.exame_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(exame: Exame) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            exame.cod_exame,
            exame.cod_doacao,
            exame.data_exame,
            exame.tipo_exame,
            exame.resultado,
            exame.arquivo)) 
        return cursor.lastrowid
    

def obter_todos() -> list[Exame]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        exame = [
            Exame(
                cod_exame=row["cod_exame"],
                cod_doacao=row["cod_doacao"],
                data_exame=row["data_exame"],
                tipo_exame=row["tipo_exame"],
                resultado=row["resultado"],
                arquivo=row["arquivo"]) 
                for row in rows]
        return exame
    
def obter_por_id(self, cod_exame: int) -> Optional[Exame]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_exame,))
        row = cursor.fetchone()
        if row:
            return Exame(
                cod_exame=row["cod_exame"],
                cod_doacao=row["cod_doacao"],
                data_exame=row["data_exame"],
                tipo_exame=row["tipo_exame"],
                resultado=row["resultado"],
                arquivo=row["arquivo"]
                ) 
        return None
    
def update(self, exame: Exame) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                exame.cod_exame,
                exame.cod_doacao,
                exame.data_exame,
                exame.tipo_exame,
                exame.resultado,
                exame.arquivo
            ),
        )
        return cursor.rowcount > 0

def delete(self, cod_exame: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_exame,))
        return cursor.rowcount > 0