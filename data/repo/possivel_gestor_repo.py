import os
from sqlite3 import Connection
from typing import Optional
from data.model.possivel_gestor_model import Possivel_Gestor
from data.sql.possivel_gestor_sql import *
from util.database import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela possivel_gestor: {e}")
        return False
    

def inserir(possivel_gestor: Possivel_Gestor) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            possivel_gestor.nome_possivel_gestor,
            possivel_gestor.email_possivel_gestor,
            possivel_gestor.telefone_possivel_gestor,
            possivel_gestor.cargo_possivel_gestor
        ))
        return cursor.lastrowid
    

def obter_todos() -> list[Possivel_Gestor]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        possiveis_gestores = [
            Possivel_Gestor(
                cod_possivel_gestor=row["cod_possivel_gestor"],
                nome_possivel_gestor=row["nome_possivel_gestor"],
                email_possivel_gestor=row["email_possivel_gestor"],
                telefone_possivel_gestor=row["telefone_possivel_gestor"],
                cargo_possivel_gestor=row["cargo_possivel_gestor"]
            )
            for row in rows]
        return possiveis_gestores
    
def obter_por_id(cod_possivel_gestor: int) -> Optional[Possivel_Gestor]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_possivel_gestor,))
        row = cursor.fetchone()
        if row:
            return Possivel_Gestor(
                cod_possivel_gestor=row["cod_possivel_gestor"],
                nome_possivel_gestor=row["nome_possivel_gestor"],
                email_possivel_gestor=row["email_possivel_gestor"],
                telefone_possivel_gestor=row["telefone_possivel_gestor"],
                cargo_possivel_gestor=row["cargo_possivel_gestor"]
            )
        return None

def obter_por_email(email_possivel_gestor: str) -> Optional[Possivel_Gestor]:
    """
    Busca um possível gestor pelo email
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMAIL, (email_possivel_gestor,))
        row = cursor.fetchone()
        if row:
            return Possivel_Gestor(
                cod_possivel_gestor=row["cod_possivel_gestor"],
                nome_possivel_gestor=row["nome_possivel_gestor"],
                email_possivel_gestor=row["email_possivel_gestor"],
                telefone_possivel_gestor=row["telefone_possivel_gestor"],
                cargo_possivel_gestor=row["cargo_possivel_gestor"]
            )
        return None

def verificar_email_existe(email_possivel_gestor: str) -> bool:
    """
    Verifica se já existe um possível gestor com o email informado
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_EMAIL_EXISTE, (email_possivel_gestor,))
        row = cursor.fetchone()
        return row["count"] > 0 if row else False

def obter_por_cargo(cargo_possivel_gestor: str) -> list[Possivel_Gestor]:
    """
    Busca possíveis gestores por cargo
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CARGO, (cargo_possivel_gestor,))
        rows = cursor.fetchall()
        possiveis_gestores = [
            Possivel_Gestor(
                cod_possivel_gestor=row["cod_possivel_gestor"],
                nome_possivel_gestor=row["nome_possivel_gestor"],
                email_possivel_gestor=row["email_possivel_gestor"],
                telefone_possivel_gestor=row["telefone_possivel_gestor"],
                cargo_possivel_gestor=row["cargo_possivel_gestor"]
            )
            for row in rows]
        return possiveis_gestores
    
def update(possivel_gestor: Possivel_Gestor) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                possivel_gestor.nome_possivel_gestor,
                possivel_gestor.email_possivel_gestor,
                possivel_gestor.telefone_possivel_gestor,
                possivel_gestor.cargo_possivel_gestor,
                possivel_gestor.cod_possivel_gestor
            ),
        )
        return cursor.rowcount > 0

def delete(cod_possivel_gestor: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_possivel_gestor,))
        return cursor.rowcount > 0
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/inserts.sql')
    if os.path.exists(caminho_arquivo_sql):
        with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
            sql_inserts = arquivo.read()
            conexao.execute(sql_inserts)
