import os
from sqlite3 import Connection
from typing import Optional
from data.repo import usuario_repo
from data.model.gestor_model import Gestor
from data.sql.gestor_sql import *
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
    

def inserir(gestor: Gestor) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(0,
            gestor.nome, 
            gestor.email, 
            gestor.senha,
            gestor.cpf,
            gestor.data_nascimento,
            gestor.status,
            gestor.data_cadastro,
            gestor.rua_usuario,
            gestor.bairro_usuario,
            gestor.cidade_usuario,
            gestor.cep_usuario,
            gestor.telefone)
        cod_gestor = usuario_repo.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            cod_gestor, 
            gestor.cnpj, 
            gestor.instituicao))
        return cod_gestor
    
def obter_todos() -> list[Gestor]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        gestor = [
            Gestor(
                cod_gestor=row["cod_gestor"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf=row["cpf"],
                data_nascimento=datetime.strptime(row["data_nascimento"], '%Y-%m-%d').date(),
                status=row["status"],
                data_cadastro=datetime.strptime(row["data_cadastro"], '%Y-%m-%d').date(),
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"],
                telefone=row["telefone"],
                cnpj=row["cnpj"],
                instituicao=row["instituicao"])  
                for row in rows]
        return gestor
    
def obter_por_id(cod_gestor: int) -> Optional[Gestor]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_gestor,))
        row = cursor.fetchone()
        gestor = Gestor(
            cod_gestor=row["cod_gestor"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            cpf=row["cpf"],
            data_nascimento=datetime.strptime(row["data_nascimento"], '%Y-%m-%d').date(),
            status=row["status"],
            data_cadastro=datetime.strptime(row["data_cadastro"], "%Y-%m-%d").date(),
            rua_usuario=row["rua_usuario"],
            bairro_usuario=row["bairro_usuario"],
            cidade_usuario=row["cidade_usuario"],
            cep_usuario=row["cep_usuario"],
            telefone=row["telefone"],
            cnpj=row["cnpj"],
            instituicao=row["instituicao"])
        return gestor
    
# def obter_todos() -> list[Gestor]:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_TODOS)
#         rows = cursor.fetchall()
#         gestor = [
#             Gestor(
#                 cod_gestor=row["cod_gestor"],
#                 nome=row["nome"],
#                 email=row["email"],
#                 senha=row["senha"],
#                 cpf=row["cpf"],
#                 data_nascimento=row["data_nascimento"],
#                 status=row["status"],
#                 data_cadastro=row["data_cadastro"],
#                 rua_usuario=row["rua_usuario"],
#                 bairro_usuario=row["bairro_usuario"],
#                 cidade_usuario=row["cidade_usuario"],
#                 cep_usuario=row["cep_usuario"],
#                 telefone=row["telefone"],
#                 cnpj=row["cnpj"],
#                 instituicao=row["instituicao"])  
#                 for row in rows]
#         return gestor
    
# def obter_por_id(cod_gestor: int) -> Optional[Gestor]:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_POR_ID, (cod_gestor,))
#         row = cursor.fetchone()
#         gestor = Gestor(
#             cod_gestor=row["cod_gestor"],
#             nome=row["nome"],
#             email=row["email"],
#             senha=row["senha"],
#             cpf=row["cpf"],
#             data_nascimento=row["data_nascimento"],
#             status=row["status"],
#             data_cadastro=row["data_cadastro"],
#             rua_usuario=row["rua_usuario"],
#             bairro_usuario=row["bairro_usuario"],
#             cidade_usuario=row["cidade_usuario"],
#             cep_usuario=row["cep_usuario"],
#             telefone=row["telefone"],
#             cnpj=row["cnpj"],
#             instituicao=row["instituicao"])
#         return gestor
    
def update(gestor: Gestor) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            gestor.cod_gestor, 
            gestor.nome, 
            gestor.email, 
            gestor.senha,
            gestor.cpf,
            gestor.data_nascimento,
            gestor.status,
            gestor.data_cadastro,
            gestor.rua_usuario,
            gestor.bairro_usuario,
            gestor.cidade_usuario,
            gestor.cep_usuario,
            gestor.telefone)
        usuario_repo.update(usuario, cursor)
        cursor.execute(UPDATE, (
            gestor.cnpj, 
            gestor.instituicao, 
            gestor.cod_gestor))
        return (cursor.rowcount > 0)

def delete(cod_gestor: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_gestor,))
        usuario_repo.delete(cod_gestor, cursor)
        return (cursor.rowcount > 0)

def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)