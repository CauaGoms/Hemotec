import os
from sqlite3 import Connection
from typing import Optional
from data.repo import usuario_repo
from data.model.colaborador_model import Colaborador
from data.sql.colaborador_sql import *
from data.model.usuario_model import Usuario
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
    

def inserir(colaborador: Colaborador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(0, 
            colaborador.nome, 
            colaborador.email, 
            colaborador.senha,
            colaborador.cpf,
            colaborador.data_nascimento,
            colaborador.status,
            colaborador.data_cadastro,
            colaborador.rua_usuario,
            colaborador.bairro_usuario,
            colaborador.cidade_usuario,
            colaborador.cep_usuario,
            colaborador.telefone)
        cod_colaborador = usuario_repo.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            cod_colaborador,
            colaborador.funcao))
        return cod_colaborador
    

def obter_todos() -> list[Colaborador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        colaborador = [
            Colaborador(
                cod_colaborador=row["cod_colaborador"],
                nome=row["nome"],
                email=row["email"],
                cod_usuario=row["cod_usuario"],
                senha=row["senha"],
                cpf=row["cpf"],
                data_nascimento=datetime.strptime(row["data_nascimento"], "%Y-%m-%d"),
                status=row["status"],
                data_cadastro=datetime.strptime(row["data_cadastro"], "%Y-%m-%d"),
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"],
                telefone=row["telefone"],
                funcao=row["funcao"])  
                for row in rows]
        return colaborador
    
def obter_por_id(cod_colaborador: int) -> Optional[Colaborador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_colaborador,))
        row = cursor.fetchone()
        if not row:
            return None
        colaborador = Colaborador(
            cod_colaborador=row["cod_colaborador"],
            funcao=row["funcao"],
            cod_usuario=row["cod_usuario"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            cpf=row["cpf"],
            data_nascimento=datetime.strptime(row["data_nascimento"], "%Y-%m-%d"),
            status=row["status"],
            data_cadastro=datetime.strptime(row["data_cadastro"], "%Y-%m-%d"),
            rua_usuario=row["rua_usuario"],
            bairro_usuario=row["bairro_usuario"],
            cidade_usuario=row["cidade_usuario"],
            cep_usuario=row["cep_usuario"],
            telefone=row["telefone"])
        return colaborador
    
def update(colaborador: Colaborador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            colaborador.cod_usuario,
            colaborador.nome, 
            colaborador.email, 
            colaborador.senha,
            colaborador.cpf,
            colaborador.data_nascimento,
            colaborador.status,
            colaborador.data_cadastro,
            colaborador.rua_usuario,
            colaborador.bairro_usuario,
            colaborador.cidade_usuario,
            colaborador.cep_usuario,
            colaborador.telefone)
        usuario_repo.update(usuario)
        cursor.execute(UPDATE, (
            colaborador.funcao,
            colaborador.cod_colaborador))
        return (cursor.rowcount > 0)

def delete(cod_colaborador: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_colaborador,))
        colaborador_removido = cursor.rowcount > 0
    usuario_repo.delete(cod_colaborador)
    return colaborador_removido
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)