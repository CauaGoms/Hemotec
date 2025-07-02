import os
from sqlite3 import Connection
from typing import Optional
from data.model.adm_campanha_model import Adm_campanha
from data.sql.adm_campanha_sql import *
from data.util.database import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela da categoria: {e}")
        return False
    

def inserir(adm_campanha: Adm_campanha, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (
            adm_campanha.cod_adm, 
            adm_campanha.cod_campanha, 
            adm_campanha.papel))
        return cursor.lastrowid
    else:
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
    
def obter_por_id(cod_adm: int) -> Optional[Adm_campanha]:
    with get_connection() as conn:
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
    
def update(adm_campanha: Adm_campanha) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                adm_campanha.cod_campanha,
                adm_campanha.papel,
                adm_campanha.cod_adm
            ),
        )
        return cursor.rowcount > 0

def delete(cod_adm: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_adm,))
        return cursor.rowcount > 0
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)