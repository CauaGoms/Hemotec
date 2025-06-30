import os
from typing import Optional
from data.model.plano_model import Plano
from data.sql.plano_sql import *
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
    

def inserir(plano: Plano) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            plano.cod_plano,
            plano.cod_assinatura,
            plano.qtd_licenca,
            plano.nome,
            plano.valor,
            plano.validade
            ))
        return cursor.lastrowid
    

def obter_todos() -> list[Plano]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        plano = [
            Plano(
                cod_plano=row["cod_plano"],
                cod_assinatura=row["cod_assinatura"],
                qtd_licenca=row["qtd_licenca"],
                nome=row["nome"],
                valor=row["valor"],
                validade=row["validade"]) 
                for row in rows]
        return plano
    
def obter_por_id(cod_plano: int) -> Optional[Plano]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_plano,))
        row = cursor.fetchone()
        if row:
            return Plano(
                cod_plano=row["cod_plano"],
                cod_assinatura=row["cod_assinatura"],
                qtd_licenca=row["qtd_licenca"],
                nome=row["nome"],
                valor=row["valor"],
                validade=row["validade"]
                )
        return None
    
def update(plano: Plano) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                plano.cod_assinatura,
                plano.qtd_licenca,
                plano.nome,
                plano.valor,
                plano.validade,
                plano.cod_plano
            ),
        )
        return cursor.rowcount > 0

def delete(cod_plano: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_plano,))
        return cursor.rowcount > 0

def inserir_dados_iniciais(conexao: get_connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)