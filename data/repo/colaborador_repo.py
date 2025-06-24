from typing import Optional
from data.repo import usuario_repo
from data.model.colaborador_model import Colaborador
from data.sql.colaborador_sql import *
from data.model.usuario_model import Usuario
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

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
            colaborador.cod_agendamento,
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
                cod_agendamento=row["cod_agendamento"],
                funcao=row["funcao"])  
                for row in rows]
        return colaborador
    
def obter_por_id(cod_colaborador: int) -> Optional[Colaborador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_colaborador,))
        row = cursor.fetchone()
        colaborador = Colaborador(
            cod_colaborador=row["cod_colaborador"],
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
            cod_agendamento=row["cod_agendamento"],
            funcao=row["funcao"])
        return colaborador
    
def update(colaborador: Colaborador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            colaborador.cod_colaborador, 
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
        usuario_repo.update(usuario, cursor)
        cursor.execute(UPDATE, (
            colaborador.cod_agendamento,
            colaborador.funcao,
            colaborador.cod_colaborador))
        return (cursor.rowcount > 0)

def delete(cod_colaborador: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_colaborador,))
        usuario_repo.delete(cod_colaborador, cursor)
        return (cursor.rowcount > 0)