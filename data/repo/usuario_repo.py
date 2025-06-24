from typing import Any, Optional
from data.model.usuario_model import Usuario
from data.sql.usuario_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

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
                data_nascimento=row["data_nascimento"],
                status=row["status"],
                data_cadastro=row["data_cadastro"],
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
                data_nascimento=row["data_nascimento"],
                status=row["status"],
                data_cadastro=row["data_cadastro"],
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cod_cidade=row["cidade_usuario"],
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
                data_nascimento=row["data_nascimento"],
                status=row["status"],
                data_cadastro=row["data_cadastro"],
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"],
                telefone=row["telefone"])
        
        return None
    
def update(usuario: Usuario, cursor:Any) -> bool:
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
        ))
    return cursor.rowcount > 0

def atualizar_senha(cod_usuario: int, senha: str, cursor: Any) -> bool:
    cursor.execute(ALTERAR_SENHA, (senha, cod_usuario))
    return (cursor.rowcount > 0)

def delete(cod_usuario: int, cursor:Any) -> bool:
    cursor.execute(DELETE, (cod_usuario,))
    return (cursor.rowcount > 0)