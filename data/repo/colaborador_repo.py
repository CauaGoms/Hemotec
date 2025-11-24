import os
from sqlite3 import Connection
from typing import Optional
from data.repo import usuario_repo
from data.model.colaborador_model import Colaborador
from data.sql.colaborador_sql import *
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
    

def inserir(colaborador: Colaborador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            cod_usuario=0,
            nome=colaborador.nome,
            email=colaborador.email,
            senha=colaborador.senha,
            cpf=colaborador.cpf,
            data_nascimento=colaborador.data_nascimento,
            status=colaborador.status,
            rua_usuario=colaborador.rua_usuario,
            bairro_usuario=colaborador.bairro_usuario,
            cidade_usuario=colaborador.cidade_usuario,
            cep_usuario=colaborador.cep_usuario,
            telefone=colaborador.telefone,
            genero='',
            perfil='colaborador',
            data_cadastro=colaborador.data_cadastro,
            foto=None,
            token_redefinicao=None,
            data_token=None,
            estado_usuario=None
        )
        cod_colaborador = usuario_repo.inserir(usuario)
        cursor.execute(INSERIR, (
            cod_colaborador,
            colaborador.cod_unidade,
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
                cod_unidade=row["cod_unidade"],
                nome=row["nome"],
                email=row["email"],
                cod_usuario=row["cod_usuario"],
                senha=row["senha"],
                cpf=row["cpf"],
                data_nascimento=datetime.strptime(row["data_nascimento"], "%Y-%m-%d") if row["data_nascimento"] else datetime.now().date(),
                status=row["status"],
                data_cadastro=datetime.strptime(row["data_cadastro"], "%Y-%m-%d").date() if row["data_cadastro"] else datetime.now().date(),
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"],
                telefone=row["telefone"],
                funcao=row["funcao"],
                genero=row["genero"] if row["genero"] else '',
                perfil=row["perfil"] if row["perfil"] else 'colaborador',
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                estado_usuario=row["estado_usuario"])  
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
            cod_unidade=row["cod_unidade"],
            funcao=row["funcao"],
            cod_usuario=row["cod_usuario"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            cpf=row["cpf"],
            data_nascimento=datetime.strptime(row["data_nascimento"], "%Y-%m-%d") if row["data_nascimento"] else datetime.now().date(),
            status=row["status"],
            data_cadastro=datetime.strptime(row["data_cadastro"], "%Y-%m-%d").date() if row["data_cadastro"] else datetime.now().date(),
            rua_usuario=row["rua_usuario"],
            bairro_usuario=row["bairro_usuario"],
            cidade_usuario=row["cidade_usuario"],
            cep_usuario=row["cep_usuario"],
            telefone=row["telefone"],
            genero=row["genero"] if row["genero"] else '',
            perfil=row["perfil"] if row["perfil"] else 'colaborador',
            foto=row["foto"],
            token_redefinicao=row["token_redefinicao"],
            data_token=row["data_token"],
            estado_usuario=row["estado_usuario"])
        return colaborador
    
def update(colaborador: Colaborador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            cod_usuario=colaborador.cod_usuario,
            nome=colaborador.nome,
            email=colaborador.email,
            senha=colaborador.senha,
            cpf=colaborador.cpf,
            data_nascimento=colaborador.data_nascimento,
            status=colaborador.status,
            rua_usuario=colaborador.rua_usuario,
            bairro_usuario=colaborador.bairro_usuario,
            cidade_usuario=colaborador.cidade_usuario,
            cep_usuario=colaborador.cep_usuario,
            telefone=colaborador.telefone,
            genero=colaborador.genero if colaborador.genero else '',
            perfil='colaborador',
            data_cadastro=colaborador.data_cadastro,
            foto=colaborador.foto,
            token_redefinicao=colaborador.token_redefinicao,
            data_token=colaborador.data_token,
            estado_usuario=colaborador.estado_usuario
        )
        usuario_repo.update(usuario, cursor)
        cursor.execute(UPDATE, (
            colaborador.funcao,
            colaborador.cod_unidade,
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