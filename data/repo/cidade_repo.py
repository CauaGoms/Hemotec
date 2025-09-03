import os
from sqlite3 import Connection
from typing import Optional
from data.model.cidade_model import Cidade
from data.sql.cidade_sql import *
from util.database import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False
    

def inserir(cidade: Cidade) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            cidade.nome_cidade, 
            cidade.sigla_estado))
        return cursor.lastrowid
    

def obter_todos() -> list[Cidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        cidade = [
            Cidade(
                cod_cidade=row["cod_cidade"],
                nome_cidade=row["nome_cidade"],
                sigla_estado=row["sigla_estado"])  
                for row in rows]
        return cidade
    
def obter_por_id(cod_cidade: int) -> Optional[Cidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_cidade,))
        row = cursor.fetchone()
        if row:
            return Cidade(
                cod_cidade=row["cod_cidade"],
                nome_cidade=row["nome_cidade"],
                sigla_estado=row["sigla_estado"]
            )
        return None
    
def obter_por_nome(nome_cidade: str) -> Optional[Cidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_NOME, (nome_cidade,))
        row = cursor.fetchone()
        if row:
            return Cidade(
                cod_cidade=row["cod_cidade"],
                nome_cidade=row["nome_cidade"],
                sigla_estado=row["sigla_estado"]
            )
        return None
    
def update(cidade: Cidade) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                cidade.nome_cidade,
                cidade.sigla_estado,
                cidade.cod_cidade
            ),
        )
        return cursor.rowcount > 0

def delete(cod_cidade: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_cidade,))
        return cursor.rowcount > 0
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)