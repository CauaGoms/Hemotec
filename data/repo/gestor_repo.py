from typing import Optional
from data.model.gestor_model import Gestor
from data.sql.gestor_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(gestor: Gestor) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            gestor.cod_gestor, 
            gestor.cnpj, 
            gestor.instituicao))
        return cursor.lastrowid
    

def obter_todos() -> list[Gestor]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        gestor = [
            Gestor(
                cod_gestor=row["cod_gestor"],
                cnpj=row["cnpj"],
                instituicao=row["instituicao"])  
                for row in rows]
        return gestor
    
def obter_por_id(self, cod_gestor: int) -> Optional[Gestor]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_gestor,))
        row = cursor.fetchone()
        if row:
            return Gestor(
                cod_gestor=row["cod_gestor"],
                cnpj=row["cnpj"],
                instituicao=row["instituicao"]
            )
        return None
    
def update(self, gestor: Gestor) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                gestor.cod_gestor,
                gestor.cnpj,
                gestor.instituicao
            ),
        )
        return cursor.rowcount > 0

def delete(self, cod_gestor: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_gestor,))
        return cursor.rowcount > 0