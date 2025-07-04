import os
from sqlite3 import Connection
from typing import Optional
from data.model.unidade_coleta_model import Unidade_coleta
from data.sql.unidade_coleta_sql import *
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
    

def inserir(unidade_coleta: Unidade_coleta) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            unidade_coleta.cod_licenca,
            unidade_coleta.nome,
            unidade_coleta.email,
            unidade_coleta.rua_unidade,
            unidade_coleta.bairro_unidade,
            unidade_coleta.cidade_unidade,
            unidade_coleta.cep_unidade,
            unidade_coleta.latitude,
            unidade_coleta.longitude,
            unidade_coleta.telefone
            ))
        return cursor.lastrowid
    

def obter_todos() -> list[Unidade_coleta]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        unidade_coleta = [
            Unidade_coleta(
                cod_unidade=row["cod_unidade"],
                cod_licenca=row["cod_licenca"],
                nome=row["nome"],
                email=row["email"],
                rua_unidade=row["rua_unidade"],
                bairro_unidade=row["bairro_unidade"],
                cidade_unidade=row["cidade_unidade"],
                cep_unidade=row["cep_unidade"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                telefone=row["telefone"]
                )  
                for row in rows]
        return unidade_coleta
    
def obter_por_id(cod_unidade_coleta: int) -> Optional[Unidade_coleta]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_unidade_coleta,))
        row = cursor.fetchone()
        if row:
            return Unidade_coleta(
                cod_unidade=row["cod_unidade"],
                cod_licenca=row["cod_licenca"],
                nome=row["nome"],
                email=row["email"],
                rua_unidade=row["rua_unidade"],
                bairro_unidade=row["bairro_unidade"],
                cidade_unidade=row["cidade_unidade"],
                cep_unidade=row["cep_unidade"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                telefone=row["telefone"]
            )
        return None
    
def obter_coordenada():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nome, latitude, longitude FROM unidade_coleta")
        resultados = cursor.fetchall()
        return [
            {row["nome"]: [row["latitude"], row["longitude"]]}
            for row in resultados
        ]

def update(unidade_coleta: Unidade_coleta) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                unidade_coleta.cod_licenca,
                unidade_coleta.nome,
                unidade_coleta.email,
                unidade_coleta.rua_unidade,
                unidade_coleta.bairro_unidade,
                unidade_coleta.cidade_unidade,
                unidade_coleta.cep_unidade,
                unidade_coleta.latitude,
                unidade_coleta.longitude,
                unidade_coleta.telefone,
                unidade_coleta.cod_unidade
            ),
        )
        return cursor.rowcount > 0

def delete(cod_unidade_coleta: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_unidade_coleta,))
        return cursor.rowcount > 0

def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)