import os
from sqlite3 import Connection
from typing import Optional
from data.model.estoque_model import Estoque
from data.sql.estoque_sql import *
from util.database import get_connection
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
    

def inserir(estoque: Estoque) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            estoque.cod_unidade, 
            estoque.tipo_sanguineo, 
            estoque.fator_rh, 
            estoque.quantidade,
            estoque.data_atualizacao))
        return cursor.lastrowid
    

def obter_todos() -> list[Estoque]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        estoque = []
        for row in rows:
            data_str = row["data_atualizacao"]
            try:
                data_atualizacao = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                data_atualizacao = datetime.strptime(data_str, '%Y-%m-%d')
        estoque = [
            Estoque(
                cod_estoque=row["cod_estoque"],
                cod_unidade=row["cod_unidade"],
                tipo_sanguineo=row["tipo_sanguineo"],
                fator_rh=row["fator_rh"],
                quantidade=row["quantidade"],
                data_atualizacao=data_atualizacao)
                for row in rows]
        return estoque
    
def obter_por_id(cod_estoque: int) -> Optional[Estoque]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_estoque,))
        row = cursor.fetchone()
        if row:
            data_str = row["data_atualizacao"]
            try:
                data_atualizacao = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                data_atualizacao = datetime.strptime(data_str, '%Y-%m-%d')
            return Estoque(
                cod_estoque=row["cod_estoque"],
                cod_unidade=row["cod_unidade"],
                tipo_sanguineo=row["tipo_sanguineo"],
                fator_rh=row["fator_rh"],
                quantidade=row["quantidade"],
                data_atualizacao=data_atualizacao
            )
        return None
    
def obter_por_unidade(cod_unidade: int) -> Optional[Estoque]:
    """
    Busca todos os registros de estoque de uma unidade específica
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Query SQL para buscar estoque por unidade
            sql = """
                SELECT cod_estoque, cod_unidade, tipo_sanguineo, fator_rh, quantidade, data_atualizacao
                FROM estoque 
                WHERE cod_unidade = ?
                ORDER BY tipo_sanguineo, fator_rh
            """
            
            cursor.execute(sql, (cod_unidade,))
            rows = cursor.fetchall()
            
            # Converte os resultados em objetos Estoque
            estoque_lista = []
            for row in rows:
                data_str = row["data_atualizacao"]
                data_atualizacao = None
                if data_str:
                    try:
                        data_atualizacao = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        data_atualizacao = datetime.strptime(data_str, '%Y-%m-%d')
                estoque = Estoque(
                    cod_estoque=row["cod_estoque"],
                    cod_unidade=row["cod_unidade"],
                    tipo_sanguineo=row["tipo_sanguineo"],
                    fator_rh=row["fator_rh"],
                    quantidade=row["quantidade"],
                    data_atualizacao=data_atualizacao
                )
                estoque_lista.append(estoque)
            
            return estoque_lista
            
    except Exception as e:
        print(f"Erro ao buscar estoque da unidade {cod_unidade}: {e}")
        return []
    
def update(estoque: Estoque) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                estoque.cod_unidade,
                estoque.tipo_sanguineo,
                estoque.fator_rh,
                estoque.quantidade,
                estoque.data_atualizacao,
                estoque.cod_estoque
            ),
        )
        return cursor.rowcount > 0

def delete(cod_estoque: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_estoque,))
        return cursor.rowcount > 0
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)