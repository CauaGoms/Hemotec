import os
from sqlite3 import Connection
from typing import Optional
from data.model.assinatura_model import Assinatura
from data.sql.assinatura_sql import *
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
    

def inserir(assinatura: Assinatura) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            assinatura.cnpj,
            assinatura.cod_plano,
            assinatura.cod_licenca,
            assinatura.data_inicio,
            assinatura.data_fim,
            assinatura.valor,
            assinatura.qtd_licenca))
        return cursor.lastrowid
    

def obter_todos() -> list[Assinatura]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        assinatura = [
            Assinatura(
                cod_assinatura=row["cod_assinatura"],
                cnpj=row["cnpj"],
                cod_plano=row["cod_plano"],
                cod_licenca=row["cod_licenca"],
                data_inicio=datetime.strptime(row["data_inicio"], '%Y-%m-%d'),
                data_fim=datetime.strptime(row["data_fim"], '%Y-%m-%d'),
                valor=row["valor"],
                qtd_licenca=row["qtd_licenca"]
                )  
                for row in rows]
        return assinatura
    
def obter_por_id(cod_assinatuta: int) -> Optional[Assinatura]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_assinatuta,))
        row = cursor.fetchone()
        if row:
            return Assinatura(
                cod_assinatura=row["cod_assinatura"],
                cnpj=row["cnpj"],
                cod_plano=row["cod_plano"],
                cod_licenca=row["cod_licenca"],
                data_inicio=datetime.strptime(row["data_inicio"], '%Y-%m-%d'),
                data_fim=datetime.strptime(row["data_fim"], '%Y-%m-%d'),
                valor=row["valor"],
                qtd_licenca=row["qtd_licenca"]
            )
        return None
    
def update(assinatura: Assinatura) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                assinatura.cnpj,
                assinatura.cod_plano,
                assinatura.cod_licenca,
                assinatura.data_inicio,
                assinatura.data_fim,
                assinatura.valor,
                assinatura.qtd_licenca,
                assinatura.cod_assinatura
            ),
        )
        return cursor.rowcount > 0

def delete(cod_assinatura: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_assinatura,))
        return cursor.rowcount > 0

def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)