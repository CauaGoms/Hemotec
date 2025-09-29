import os
from sqlite3 import Connection
from typing import Optional
from data.repo import usuario_repo
from data.model.doador_model import Doador
from data.sql.doador_sql import *
from data.model.usuario_model import Usuario
from util.database import get_connection
from datetime import date, datetime

def criar_tabela(cursor=None) -> bool:
    try:
        if cursor is not None:
            cursor.execute(CRIAR_TABELA)
        else:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(CRIAR_TABELA)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela doador: {e}")
        return False
    

def inserir(doador: Doador, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(
            INSERIR,
            (
                doador.cod_doador,
                doador.tipo_sanguineo,
                doador.fator_rh,
                doador.elegivel,
                doador.altura,
                doador.peso,
                doador.profissao,
                doador.contato_emergencia,
                doador.telefone_emergencia,
            ),
        )
        return cursor.lastrowid
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                INSERIR,
                (
                    doador.cod_doador,
                    doador.tipo_sanguineo,
                    doador.fator_rh,
                    doador.elegivel,
                    doador.altura,
                    doador.peso,
                    doador.profissao,
                    doador.contato_emergencia,
                    doador.telefone_emergencia,
                ),
            )
            return cursor.lastrowid
    

def obter_todos() -> list[Doador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        doador = [
            Doador(
                cod_doador=row["cod_doador"],
                cod_usuario=row["cod_doador"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf=row["cpf"],
                data_nascimento=datetime.strptime(row["data_nascimento"], "%Y-%m-%d").date() if isinstance(row["data_nascimento"], str) else row["data_nascimento"],
                status=row["status"],
                data_cadastro=datetime.strptime(row["data_cadastro"], "%Y-%m-%d").date() if isinstance(row["data_cadastro"], str) else row["data_cadastro"],
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"],
                telefone=row["telefone"],
                tipo_sanguineo=row["tipo_sanguineo"],
                fator_rh=row["fator_rh"],
                elegivel=row["elegivel"],
                altura=row["altura"],
                peso=row["peso"],
                profissao=row["profissao"],
                contato_emergencia=row["contato_emergencia"],
                telefone_emergencia=row["telefone_emergencia"])
            for row in rows]
        return doador

def obter_por_id(cod_doador: int) -> Optional[Doador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_doador,))
        row = cursor.fetchone()
        if row:
            # Criar objeto Usuario primeiro
            usuario = Usuario(
                cod_usuario=row["cod_doador"],  # ou row["cod_usuario"] se existir
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf=row["cpf"],
                data_nascimento=datetime.strptime(row["data_nascimento"], "%Y-%m-%d").date() if isinstance(row["data_nascimento"], str) else row["data_nascimento"],
                status=row["status"],
                rua_usuario=row["rua_usuario"],
                bairro_usuario=row["bairro_usuario"],
                cidade_usuario=row["cidade_usuario"],
                cep_usuario=row["cep_usuario"],
                telefone=row["telefone"],
                data_cadastro=datetime.strptime(row["data_cadastro"], "%Y-%m-%d").date() if isinstance(row["data_cadastro"], str) else row["data_cadastro"]
            )
            
            # Criar objeto Doador com Usuario
            doador = Doador(
                cod_doador=row["cod_doador"],
                usuario=usuario,
                tipo_sanguineo=row["tipo_sanguineo"],
                fator_rh=row["fator_rh"],
                elegivel=row["elegivel"],
                altura=row["altura"],
                peso=row["peso"],
                profissao=row["profissao"],
                contato_emergencia=row["contato_emergencia"],
                telefone_emergencia=row["telefone_emergencia"])
            return doador
        return None
    
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
            doador.tipo_sanguineo,
            doador.fator_rh,
            doador.elegivel,
            doador.altura,
            doador.peso,
            doador.profissao,
            doador.contato_emergencia,
            doador.telefone_emergencia,
            doador.cod_doador))
        return (cursor.rowcount > 0)

def delete(cod_doador: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_doador,))
        usuario_repo.delete(cod_doador, cursor)
        return (cursor.rowcount > 0)

def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)

# def calcular_idade(data_nascimento: str) -> int:
#     # data_nascimento no formato 'YYYY-MM-DD'
#     nascimento = date.fromisoformat(data_nascimento)
#     hoje = date.today()
#     idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
#     return idade

# def verificar_idade_doador(cod_doador: int) -> bool:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_IDADE, (cod_doador,))
#         row = cursor.fetchone()
#         if row:
#             idade = calcular_idade(row["data_nascimento"])
#             # Critério: idade entre 16 e 69 anos
#             return 16 <= idade <= 69
#         return False