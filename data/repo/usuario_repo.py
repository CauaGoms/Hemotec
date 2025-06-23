from typing import Optional
from data.model.usuario_model import Usuario
from data.sql.usuario_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
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
            usuario.cep_usuario))
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
                data_nascimento=row["data_nascimento"],
                status=row["status"],
                data_cadastro=row["data_cadastro"],
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"])  
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
                data_nascimento=row["data_nascimento"],
                status=row["status"],
                data_cadastro=row["data_cadastro"],
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cod_cidade=row["cod_cidade"],
                cep_usuario=row["cep_usuario"]
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
                data_nascimento=row["data_nascimento"],
                status=row["status"],
                data_cadastro=row["data_cadastro"],
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"])
        
        return None
    
def update(usuario: Usuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                usuario.cod_usuario,
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
                usuario.cep_usuario
            ),
        )
        return cursor.rowcount > 0

def delete(cod_usuario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_usuario,))
        return cursor.rowcount > 0