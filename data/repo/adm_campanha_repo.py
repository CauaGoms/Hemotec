from typing import Optional
from data.model.adm_campanha_model import Adm_campanha
from data.sql.adm_campanha_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(adm_campanha: Adm_campanha) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            adm_campanha.cod_adm, 
            adm_campanha.cod_campanha, 
            adm_campanha.papel))
        return cursor.lastrowid
    

def obter_todos() -> list[Adm_campanha]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        adm_campanha = [
            Adm_campanha(
                cod_adm=row["cod_adm"],
                cod_campanha=row["cod_campanha"],
                papel=row["papel"])  
                for row in rows]
        return adm_campanha
    
def obter_por_id(self, cod_adm: int) -> Optional[Adm_campanha]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_adm,))
        row = cursor.fetchone()
        if row:
            return Adm_campanha(
                cod_adm=row["cod_adm"],
                cod_campanha=row["cod_campanha"],
                papel=row["papel"]
            )
        return None
    
def update(self, adm_campanha: Adm_campanha) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                adm_campanha.cod_adm,
                adm_campanha.cod_campanha,
                adm_campanha.papel
            ),
        )
        return cursor.rowcount > 0

def delete(self, cod_adm: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_adm,))
        return cursor.rowcount > 0