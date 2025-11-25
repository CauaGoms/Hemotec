import os
from sqlite3 import Connection
from typing import Optional
from data.model.adm_unidade_model import Adm_unidade
from data.sql.adm_unidade_sql import *
from data.model.usuario_model import Usuario
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
    

def inserir(adm_unidade: Adm_unidade, cursor=None) -> Optional[int]:
    from data.repo import usuario_repo
    
    # Criar objeto Usuario com todos os campos necessários
    usuario = Usuario(
        cod_usuario=0,
        nome=adm_unidade.nome, 
        email=adm_unidade.email, 
        senha=adm_unidade.senha,
        cpf=adm_unidade.cpf,
        data_nascimento=adm_unidade.data_nascimento,
        status=adm_unidade.status,
        rua_usuario=adm_unidade.rua_usuario,
        bairro_usuario=adm_unidade.bairro_usuario,
        cidade_usuario=adm_unidade.cidade_usuario,
        cep_usuario=adm_unidade.cep_usuario,
        telefone=adm_unidade.telefone,
        genero=adm_unidade.genero or '',
        perfil='adm_unidade',
        data_cadastro=adm_unidade.data_cadastro,
        foto=adm_unidade.foto,
        estado_usuario=None
    )
    
    # Inserir usuário primeiro (cria sua própria transação)
    cod_adm_unidade = usuario_repo.inserir(usuario)
    
    # Depois inserir na tabela adm_unidade
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            cod_adm_unidade,
            adm_unidade.cod_unidade, 
            adm_unidade.permissao_envio_campanha,
            adm_unidade.permissao_envio_notificacao))
        conn.commit()
    
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
    from data.repo import usuario_repo
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            cod_usuario=adm_unidade.cod_adm, 
            nome=adm_unidade.nome, 
            email=adm_unidade.email, 
            senha=adm_unidade.senha,
            cpf=adm_unidade.cpf,
            data_nascimento=adm_unidade.data_nascimento,
            status=adm_unidade.status,
            rua_usuario=adm_unidade.rua_usuario,
            bairro_usuario=adm_unidade.bairro_usuario,
            cidade_usuario=adm_unidade.cidade_usuario,
            cep_usuario=adm_unidade.cep_usuario,
            telefone=adm_unidade.telefone,
            genero=adm_unidade.genero,
            perfil=adm_unidade.perfil,
            data_cadastro=adm_unidade.data_cadastro,
            foto=adm_unidade.foto,
            token_redefinicao=None,
            data_token=None,
            estado_usuario=None)
        usuario_repo.update(usuario, cursor)
        cursor.execute(UPDATE, (
            adm_unidade.cod_unidade,
            adm_unidade.permissao_envio_campanha,
            adm_unidade.permissao_envio_notificacao,
            adm_unidade.cod_adm))
        return (cursor.rowcount > 0)

def delete(cod_adm: int) -> bool:
    from data.repo import usuario_repo
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