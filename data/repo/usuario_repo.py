from typing import Any, Optional
from data.model.usuario_model import Usuario
from data.sql.usuario_sql import *
from util.database import get_connection
from datetime import datetime
import os
from sqlite3 import Connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela da categoria: {e}")
        return False
    

def inserir(usuario: Usuario, cursor: Any) -> Optional[int]:
    cursor.execute(INSERIR, (
        usuario.nome,
        usuario.email, 
        usuario.senha,
        usuario.cpf,
        usuario.data_nascimento,
        usuario.status,
        usuario.data_cadastro,
        usuario.rua_usuario,
        usuario.bairro_usuario,
        usuario.cidade_usuario,
        usuario.cep_usuario,
        usuario.telefone))
    return cursor.lastrowid
    

def obter_todos() -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        usuario = [
            Usuario(
                cod_usuario=row["cod_usuario"],
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
                telefone=row["telefone"])  
                for row in rows]
        return usuario
    
def obter_por_id(cod_usuario: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_usuario,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                cod_usuario=row["cod_usuario"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf=row["cpf"],
                data_nascimento=datetime.strptime(row["data_nascimento"], "%Y-%m-%d").date(),
                status=row["status"],
                data_cadastro=datetime.strptime(row["data_cadastro"], "%Y-%m-%d").date(),
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"],
                telefone=row["telefone"]
            )
        return None
    
def obter_por_email(email: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_EMAIL, (email,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                cod_usuario=row["cod_usuario"],  
                nome=row["nome"],         
                email=row["email"],
                senha=row["senha"],
                cpf=row["cpf"],
                data_nascimento=datetime.strptime(row["data_nascimento"], "%Y-%m-%d").date(),
                status=row["status"],
                data_cadastro=datetime.strptime(row["data_cadastro"], "%Y-%m-%d").date(),
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"],
                telefone=row["telefone"])
        return None
    
def update(usuario: Usuario, cursor=None) -> bool:
    if cursor is not None:
        cursor.execute(
            UPDATE,
            (
                usuario.nome,
                usuario.email,
                usuario.senha,
                usuario.cpf,
                usuario.data_nascimento,
                usuario.status,
                usuario.data_cadastro,
                usuario.rua_usuario,
                usuario.bairro_usuario,
                usuario.cidade_usuario,
                usuario.cep_usuario,
                usuario.telefone,
                usuario.cod_usuario
            )
        )
        return cursor.rowcount > 0
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                UPDATE,
                (
                    usuario.nome,
                    usuario.email,
                    usuario.senha,
                    usuario.cpf,
                    usuario.data_nascimento,
                    usuario.status,
                    usuario.data_cadastro,
                    usuario.rua_usuario,
                    usuario.bairro_usuario,
                    usuario.cidade_usuario,
                    usuario.cep_usuario,
                    usuario.telefone,
                    usuario.cod_usuario
                )
            )
            return cursor.rowcount > 0

def atualizar_senha(cod_usuario: int, senha: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_SENHA, (senha, cod_usuario))
    return (cursor.rowcount > 0)

def delete(cod_usuario: int, cursor=None) -> bool:
    if cursor is None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETE, (cod_usuario,))
            return cursor.rowcount > 0
    else:
        cursor.execute(DELETE, (cod_usuario,))
        return cursor.rowcount > 0

"""def inserir_dados_iniciais(conexao: Connection) -> None:
    # Verifica se já existem categorias na tabela
    lista = obter_todos()
    # Se já houver categorias, não faz nada
    if lista: 
        return
    # Constrói caminho para arquivo SQL com dados iniciais
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    # Abre arquivo SQL para leitura
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        # Lê conteúdo do arquivo SQL
        sql_inserts = arquivo.read()
        # Executa comandos SQL de inserção
        conexao.execute(sql_inserts)"""