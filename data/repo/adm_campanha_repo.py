from typing import Optional
from data.model.adm_campanha_model import Adm_campanha
from data.sql.adm_campanha_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(adm_campanha: Adm_campanha) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            adm_campanha.nome, 
            adm_campanha.cpf, 
            adm_campanha.email, 
            adm_campanha.telefone, 
            adm_campanha.senha))
        return cursor.lastrowid
    

def obter_todos() -> list[Cliente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        clientes = [
            Cliente(
                id=row["id"], 
                nome=row["nome"], 
                cpf=row["cpf"],
                email=row["email"],
                telefone=row["telefone"],
                senha=row["senha"]) 
                for row in rows]
        return clientes