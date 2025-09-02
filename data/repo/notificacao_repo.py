import os
from sqlite3 import Connection
from typing import Optional
from data.model.notificacao_model import Notificacao
from data.sql.notificacao_sql import *
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
    

def inserir(notificacao: Notificacao, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (
            notificacao.cod_adm,
            notificacao.tipo,
            notificacao.mensagem,
            notificacao.status,
            notificacao.data_envio
        ))
        return cursor.lastrowid
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                notificacao.cod_adm,
                notificacao.tipo,
                notificacao.mensagem,
                notificacao.status,
                notificacao.data_envio
            ))
            return cursor.lastrowid
    

def obter_todos() -> list[Notificacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        notificacao = [
            Notificacao(
                cod_notificacao=row["cod_notificacao"],
                cod_adm=row["cod_adm"],
                tipo=row["tipo"],
                mensagem=row["mensagem"],
                status=row["status"],
                data_envio=datetime.strptime(row["data_envio"], '%Y-%m-%d')) 
                for row in rows]
        return notificacao
    
def obter_por_id(cod_notificacao: int) -> Optional[Notificacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_notificacao,))
        row = cursor.fetchone()
        if row:
            data_envio_str = row["data_envio"]
            try:
                data_envio = datetime.strptime(data_envio_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                data_envio = datetime.strptime(data_envio_str, '%Y-%m-%d')
            return Notificacao(
                cod_notificacao=row["cod_notificacao"],
                cod_adm=row["cod_adm"],
                tipo=row["tipo"],
                mensagem=row["mensagem"],
                status=row["status"],
                data_envio=data_envio
                ) 
        return None
    
def update(notificacao: Notificacao) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                notificacao.cod_adm,
                notificacao.tipo,
                notificacao.mensagem,
                notificacao.status,
                notificacao.data_envio,
                notificacao.cod_notificacao
            ),
        )
        return cursor.rowcount > 0

def delete(cod_notificacao: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_notificacao,))
        return cursor.rowcount > 0
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)