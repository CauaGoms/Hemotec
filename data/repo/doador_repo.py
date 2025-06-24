from typing import Optional
from data.repo import usuario_repo
from data.model.doador_model import Doador
from data.sql.doador_sql import *
from data.model.usuario_model import Usuario
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(doador: Doador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(0, 
            doador.nome, 
            doador.email, 
            doador.senha,
            doador.cpf,
            doador.data_nascimento,
            doador.status,
            doador.data_cadastro,
            doador.rua_usuario,
            doador.bairro_usuario,
            doador.cidade_usuario,
            doador.cep_usuario,
            doador.telefone)
        cod_doador = usuario_repo.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            cod_doador, 
            doador.cod_doacao, 
            doador.cod_agendamento,
            doador.tipo_sanguineo,
            doador.fator_rh,
            doador.elegivel))
        return cod_doador
    

def obter_todos() -> list[Doador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        doador = [
            Doador(
                cod_doador=row["cod_doador"],
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
                cod_doacao=row["cod_doacao"],
                cod_agendamento=row["cod_agendamento"],
                tipo_sanguineo=row["tipo_sanguineo"],
                fator_rh=row["fator_rh"],
                elegivel=row["elegivel"])
                for row in rows]
        return doador
    
def obter_por_id(cod_doador: int) -> Optional[Doador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_doador,))
        row = cursor.fetchone()
        doador = Doador(
            cod_doador=row["cod_doador"],
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
            cod_doacao=row["cod_doacao"],
            cod_agendamento=row["cod_agendamento"],
            tipo_sanguineo=row["tipo_sanguineo"],
            fator_rh=row["fator_rh"],
            elegivel=row["elegivel"])
        return doador
    
def update(doador: Doador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            doador.cod_doador, 
            doador.nome, 
            doador.email, 
            doador.senha,
            doador.cpf,
            doador.data_nascimento,
            doador.status,
            doador.data_cadastro,
            doador.rua_usuario,
            doador.bairro_usuario,
            doador.cidade_usuario,
            doador.cep_usuario,
            doador.telefone)
        usuario_repo.update(usuario, cursor)
        cursor.execute(UPDATE, (
            doador.cod_doacao, 
            doador.cod_agendamento,
            doador.tipo_sanguineo,
            doador.fator_rh,
            doador.elegivel,
            doador.cod_doador))
        return (cursor.rowcount > 0)

def delete(cod_doador: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_doador,))
        usuario_repo.delete(cod_doador, cursor)
        return (cursor.rowcount > 0)