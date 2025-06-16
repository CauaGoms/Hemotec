from typing import Optional
from data.model.unidade_coleta_model import Unidade_coleta
from data.sql.unidade_coleta_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(unidade_coleta: Unidade_coleta) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            unidade_coleta.cod_unidade,
            unidade_coleta.cod_adm,
            unidade_coleta.cod_licenca,
            unidade_coleta.cod_estoque,
            unidade_coleta.nome,
            unidade_coleta.email,
            unidade_coleta.rua_unidade,
            unidade_coleta.bairro_unidade,
            unidade_coleta.cidade_unidade,
            unidade_coleta.cep_unidade))
        return cursor.lastrowid
    

def obter_todos() -> list[Unidade_coleta]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        unidade_coleta = [
            Unidade_coleta(
                cod_unidade_coleta=row["cod_unidade_coleta"],
                cod_adm=row["cod_adm"],
                cod_licenca=row["cod_licenca"],
                cod_estoque=row["cod_estoque"],
                nome=row["nome"],
                email=row["email"],
                rua_unidade=row["rua_unidade"],
                bairro_unidade=row["bairro_unidade"],
                cidade_unidade=row["cidade_unidade"],
                cep_unidade=row["cep_unidade"]
                )  
                for row in rows]
        return unidade_coleta
    
def obter_por_id(self, cod_unidade_coleta: int) -> Optional[Unidade_coleta]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_unidade_coleta,))
        row = cursor.fetchone()
        if row:
            return Unidade_coleta(
                cod_unidade_coleta=row["cod_unidade_coleta"],
                cod_adm=row["cod_adm"],
                cod_licenca=row["cod_licenca"],
                cod_estoque=row["cod_estoque"],
                nome=row["nome"],
                email=row["email"],
                rua_unidade=row["rua_unidade"],
                bairro_unidade=row["bairro_unidade"],
                cidade_unidade=row["cidade_unidade"],
                cep_unidade=row["cep_unidade"]
            )
        return None
    
def update(self, unidade_coleta: Unidade_coleta) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                unidade_coleta.cod_unidade,
                unidade_coleta.cod_adm,
                unidade_coleta.cod_licenca,
                unidade_coleta.cod_estoque,
                unidade_coleta.nome,
                unidade_coleta.email,
                unidade_coleta.rua_unidade,
                unidade_coleta.bairro_unidade,
                unidade_coleta.cidade_unidade,
                unidade_coleta.cep_unidade
            ),
        )
        return cursor.rowcount > 0

def delete(self, cod_unidade_coleta: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_unidade_coleta,))
        return cursor.rowcount > 0