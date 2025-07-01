import os
from sqlite3 import Connection
from typing import Optional
from data.model.doacao_model import Doacao
from data.sql.doacao_sql import *
from data.util.database import get_connection
from datetime import datetime

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela da categoria: {e}")
        return False
    

def inserir(doacao: Doacao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            doacao.cod_doador,
            doacao.data_hora,
            doacao.quantidade,
            doacao.status)) 
        return cursor.lastrowid
    

def obter_todos() -> list[Doacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        doacao = [
            Doacao(
                cod_doacao=row["cod_doacao"],
                cod_doador=row["cod_doador"],
                data_hora=datetime.strptime(row["data_hora"], '%Y-%m-%d %H:%M:%S'),
                quantidade=row["quantidade"],
                status=row["status"])  
                for row in rows]
        return doacao
    
def obter_por_id(cod_doacao: int) -> Optional[Doacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_doacao,))
        row = cursor.fetchone()
        if row:
            return Doacao(
                cod_doacao=row["cod_doacao"],
                cod_doador=row["cod_doador"],
                data_hora=datetime.strptime(row["data_hora"], '%Y-%m-%d %H:%M:%S'),
                quantidade=row["quantidade"],
                status=row["status"]
            )
        return None
    
def update(doacao: Doacao) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                doacao.cod_doador,
                doacao.data_hora,
                doacao.quantidade,
                doacao.status,
                doacao.cod_doacao
            ),
        )
        return cursor.rowcount > 0

def delete(cod_doacao: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_doacao,))
        return cursor.rowcount > 0

def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)
