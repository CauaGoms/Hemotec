import os
from sqlite3 import Connection
from typing import Optional
from data.repo import usuario_repo
from data.model.adm_unidade_model import Adm_unidade
from data.sql.adm_unidade_sql import *
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
    

def inserir(adm_unidade: Adm_unidade, cursor=None) -> Optional[int]:
    if cursor is not None:
        usuario = Usuario(0, 
            adm_unidade.nome, 
            adm_unidade.email, 
            adm_unidade.senha,
            adm_unidade.cpf,
            adm_unidade.data_nascimento,
            adm_unidade.status,
            adm_unidade.data_cadastro,
            adm_unidade.rua_usuario,
            adm_unidade.bairro_usuario,
            adm_unidade.cidade_usuario,
            adm_unidade.cep_usuario,
            adm_unidade.telefone)
        cod_adm_unidade = usuario_repo.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            cod_adm_unidade,
            adm_unidade.cod_unidade, 
            adm_unidade.permissao_envio_campanha,
            adm_unidade.permissao_envio_notificacao))
        return cod_adm_unidade
        
    elif cursor is None:
        with get_connection() as conn:
            cursor = conn.cursor()
            usuario = Usuario(0, 
                adm_unidade.nome, 
                adm_unidade.email, 
                adm_unidade.senha,
                adm_unidade.cpf,
                adm_unidade.data_nascimento,
                adm_unidade.status,
                adm_unidade.data_cadastro,
                adm_unidade.rua_usuario,
                adm_unidade.bairro_usuario,
                adm_unidade.cidade_usuario,
                adm_unidade.cep_usuario,
                adm_unidade.telefone)
            cod_adm_unidade = usuario_repo.inserir(usuario, cursor)
            cursor.execute(INSERIR, (
                cod_adm_unidade,
                adm_unidade.cod_unidade, 
                adm_unidade.permissao_envio_campanha,
                adm_unidade.permissao_envio_notificacao))
            return cod_adm_unidade
    

def obter_todos() -> list[Adm_unidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        adm_unidade = [
            Adm_unidade(
                cod_adm=row["cod_adm"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf=row["cpf"],
                data_nascimento=row["data_nascimento"],
                status=row["status"],
                data_cadastro=row["data_cadastro"],
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"],
                telefone=row["telefone"],
                cod_unidade=row["cod_unidade"],
                permissao_envio_campanha=row["permissao_envio_campanha"],
                permissao_envio_notificacao=row["permissao_envio_notificacao"])  
                for row in rows]
        return adm_unidade
    
def obter_por_id(cod_adm: int) -> Optional[Adm_unidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_adm,))
        row = cursor.fetchone()
        if row is None:
            return None
        # Converta as datas de string para date
        data_nascimento = row["data_nascimento"]
        if isinstance(data_nascimento, str):
            data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        data_cadastro = row["data_cadastro"]
        if isinstance(data_cadastro, str):
            data_cadastro = datetime.strptime(data_cadastro, "%Y-%m-%d").date()
        adm_unidade = Adm_unidade(
            cod_usuario=row["cod_adm"],
            cod_adm=row["cod_adm"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            cpf=row["cpf"],
            data_nascimento=data_nascimento,
            status=row["status"],
            data_cadastro=data_cadastro,
            rua_usuario=row["rua_usuario"],
            bairro_usuario=row["bairro_usuario"],
            cidade_usuario=row["cidade_usuario"],
            cep_usuario=row["cep_usuario"],
            telefone=row["telefone"],
            cod_unidade=row["cod_unidade"],
            permissao_envio_campanha=row["permissao_envio_campanha"],
            permissao_envio_notificacao=row["permissao_envio_notificacao"])
        return adm_unidade
    
def update(adm_unidade: Adm_unidade) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            adm_unidade.cod_adm, 
            adm_unidade.nome, 
            adm_unidade.email, 
            adm_unidade.senha,
            adm_unidade.cpf,
            adm_unidade.data_nascimento,
            adm_unidade.status,
            adm_unidade.data_cadastro,
            adm_unidade.rua_usuario,
            adm_unidade.bairro_usuario,
            adm_unidade.cidade_usuario,
            adm_unidade.cep_usuario,
            adm_unidade.telefone)
        usuario_repo.update(usuario)
        cursor.execute(UPDATE, (
            adm_unidade.cod_unidade,
            adm_unidade.permissao_envio_campanha,
            adm_unidade.permissao_envio_notificacao,
            adm_unidade.cod_adm))
        return (cursor.rowcount > 0)

def delete(cod_adm: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_adm,))
        usuario_repo.delete(cod_adm, cursor)
        return (cursor.rowcount > 0)
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)