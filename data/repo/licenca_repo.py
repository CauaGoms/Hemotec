import os
from typing import Optional
from data.model.licenca_model import Licenca
from data.sql.licenca_sql import *
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
    

def inserir(licenca: Licenca) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            licenca.cod_licenca,
            licenca.cod_assinatura,
            licenca.cod_unidade,
            licenca.status))
        return cursor.lastrowid
    

def obter_todos() -> list[Licenca]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        licenca = [
            Licenca(
                cod_licenca=row["cod_licenca"],
                cod_assinatura=row["cod_assinatura"],
                cod_unidade=row["cod_unidade"],
                status=row["status"]) 
                for row in rows]
        return licenca
    
def obter_por_id(cod_licenca: int) -> Optional[Licenca]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_licenca,))
        row = cursor.fetchone()
        if row:
            return Licenca(
                cod_licenca=row["cod_licenca"],
                cod_assinatura=row["cod_assinatura"],
                cod_unidade=row["cod_unidade"],
                status=row["status"]
                ) 
        return None
    
def update(licenca: Licenca) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                licenca.cod_assinatura,
                licenca.cod_unidade,
                licenca.status,
                licenca.cod_licenca
            ),
        )
        return cursor.rowcount > 0

def delete(cod_licenca: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_licenca,))
        return cursor.rowcount > 0
    
def inserir_dados_iniciais(conexao: get_connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)