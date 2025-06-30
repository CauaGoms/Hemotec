import os
from typing import Optional
from data.model.campanha_model import Campanha
from data.sql.campanha_sql import *
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
    

def inserir(campanha: Campanha) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            campanha.titulo, 
            campanha.descricao, 
            campanha.data_inicio, 
            campanha.data_fim,
            campanha.status))
        return cursor.lastrowid
    

def obter_todos() -> list[Campanha]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        campanha = [
            Campanha(
                cod_campanha=row["cod_campanha"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data_inicio=datetime.strptime(row["data_inicio"], "%Y-%m-%d").date(),
                data_fim=datetime.strptime(row["data_fim"], "%Y-%m-%d").date(),
                status=row["status"])  
                for row in rows]
        return campanha
    
    
def obter_por_id(cod_campanha: int) -> Optional[Campanha]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_campanha,))
        row = cursor.fetchone()
        if row:
            return Campanha(
                cod_campanha=row["cod_campanha"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data_inicio=datetime.strptime(row["data_inicio"], "%Y-%m-%d").date(),
                data_fim=datetime.strptime(row["data_fim"], "%Y-%m-%d").date(),
                status=row["status"]
            )
        return None

# def obter_todos() -> list[Campanha]:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_TODOS)
#         rows = cursor.fetchall()
#         campanha = [
#             Campanha(
#                 cod_campanha=row["cod_campanha"],
#                 titulo=row["titulo"],
#                 descricao=row["descricao"],
#                 data_inicio=row["data_inicio"],
#                 data_fim=row["data_fim"],
#                 status=row["status"])  
#                 for row in rows]
#         return campanha
#
# def obter_por_id(cod_campanha: int) -> Optional[Campanha]:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_POR_ID, (cod_campanha,))
#         row = cursor.fetchone()
#         if row:
#             return Campanha(
#                 cod_campanha=row["cod_campanha"],
#                 titulo=row["titulo"],
#                 descricao=row["descricao"],
#                 data_inicio=row["data_inicio"],
#                 data_fim=row["data_fim"],
#                 status=row["status"]
#             )
#         return None
    
def update(campanha: Campanha) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                campanha.titulo,
                campanha.descricao,
                campanha.data_inicio,
                campanha.data_fim,
                campanha.status,
                campanha.cod_campanha
            ),
        )
        return cursor.rowcount > 0

def delete(cod_campanha: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_campanha,))
        return cursor.rowcount > 0
    
def inserir_dados_iniciais(conexao: get_connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)