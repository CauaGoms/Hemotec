from typing import Optional
from data.repo import usuario_repo
from data.model.adm_unidade_model import Adm_unidade
from data.sql.adm_unidade_sql import *
from data.model.usuario_model import Usuario
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(adm_unidade: Adm_unidade) -> Optional[int]:
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
            adm_unidade.cod_notificacao,
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
                cod_notificacao=row["cod_notificacao"],
                permissao_envio_campanha=row["permissao_envio_campanha"],
                permissao_envio_notificacao=row["permissao_envio_notificacao"])  
                for row in rows]
        return adm_unidade
    
def obter_por_id(cod_adm: int) -> Optional[Adm_unidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_adm,))
        row = cursor.fetchone()
        adm_unidade = Adm_unidade(
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
            cod_notificacao=row["cod_notificacao"],
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
        usuario_repo.update(usuario, cursor)
        cursor.execute(UPDATE, (
            adm_unidade.cod_adm,
            adm_unidade.cod_unidade,
            adm_unidade.cod_notificacao,
            adm_unidade.permissao_envio_campanha,
            adm_unidade.permissao_envio_notificacao))
        return (cursor.rowcount > 0)

def delete(cod_adm: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_adm,))
        usuario_repo.delete(cod_adm, cursor)
        return (cursor.rowcount > 0)