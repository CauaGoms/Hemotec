import os
from sqlite3 import Connection
from typing import Optional
from data.model.exame_model import Exame
from data.sql.exame_sql import *
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
    
def obter_por_id(cod_exame: int) -> Optional[Exame]:
    with get_connection() as conn:
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
    
def update(exame: Exame) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                exame.cod_doacao,
                exame.data_exame,
                exame.tipo_exame,
                exame.resultado,
                exame.arquivo,
                exame.cod_exame
            ),
        )
        return cursor.rowcount > 0

def delete(cod_exame: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_exame,))
        return cursor.rowcount > 0
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)