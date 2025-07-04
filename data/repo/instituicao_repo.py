import os
from sqlite3 import Connection
from typing import Optional
from data.model.instituicao_model import Instituicao
from data.sql.instituicao_sql import *
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
    

def inserir(instituicao: Instituicao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            instituicao.cnpj,
            instituicao.nome,
            instituicao.email,
            instituicao.rua_instituicao,
            instituicao.bairro_instituicao,
            instituicao.cidade_instituicao,
            instituicao.cep_instituicao,
            instituicao.telefone))
        return cursor.lastrowid
    

def obter_todos() -> list[Instituicao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        instituicao = [
            Instituicao(
                cod_instituicao=row[0],
                cnpj=row["cnpj"],
                nome=row["nome"],
                email=row["email"],
                rua_instituicao=row["rua_instituicao"],
                bairro_instituicao=row["bairro_instituicao"],
                cidade_instituicao=row["cidade_instituicao"],
                cep_instituicao=row["cep_instituicao"],
                telefone=row["telefone"])  
                for row in rows]
        return instituicao
    
def obter_por_id(cod_instituicao: int) -> Optional[Instituicao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_instituicao,))
        row = cursor.fetchone()
        if row:
            return Instituicao(
                cod_instituicao=row["cod_instituicao"],
                cnpj=row["cnpj"],
                nome=row["nome"],
                email=row["email"],
                rua_instituicao=row["rua_instituicao"],
                bairro_instituicao=row["bairro_instituicao"],
                cidade_instituicao=row["cidade_instituicao"],
                cep_instituicao=row["cep_instituicao"],
                telefone=row["telefone"]
            )
        return None
    
def update(instituicao: Instituicao) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                instituicao.cnpj,
                instituicao.nome,
                instituicao.email,
                instituicao.rua_instituicao,
                instituicao.bairro_instituicao,
                instituicao.cep_instituicao,
                instituicao.telefone,
                instituicao.cod_instituicao
            ),
        )
        return cursor.rowcount > 0

def delete(cod_instituicao: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_instituicao,))
        return cursor.rowcount > 0

def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)