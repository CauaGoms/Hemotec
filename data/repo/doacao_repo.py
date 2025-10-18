import os
from sqlite3 import Connection
from typing import Optional
from data.model.doacao_model import Doacao
from data.sql.doacao_sql import *
from util.database import get_connection
from datetime import datetime

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
        print(f"Erro ao criar tabela doacao: {e}")
        return False
    

def inserir(doacao: Doacao, cursor=None) -> Optional[int]:
    if cursor is not None:
        cursor.execute(INSERIR, (
            doacao.cod_doador,
            doacao.cod_agendamento,
            doacao.data_hora,
            doacao.quantidade,
            doacao.status,
            doacao.observacoes
        ))
        return cursor.lastrowid
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR, (
                doacao.cod_doador,
                doacao.cod_agendamento,
                doacao.data_hora,
                doacao.quantidade,
                doacao.status,
                doacao.observacoes
            ))
            return cursor.lastrowid
    

def obter_todos() -> list[Doacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        doacao = []
        for row in rows:
            # Tentar parse com hora, se falhar tentar apenas data
            try:
                data_hora = datetime.strptime(row["data_hora"], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    data_hora = datetime.strptime(row["data_hora"], '%Y-%m-%d')
                except ValueError:
                    data_hora = None
            
            doacao.append(Doacao(
                cod_doacao=row["cod_doacao"],
                cod_doador=row["cod_doador"],
                cod_agendamento=row["cod_agendamento"],
                data_hora=data_hora,
                quantidade=row["quantidade"],
                status=row["status"],
                observacoes=row["observacoes"]
            ))
        return doacao
    
def obter_por_id(cod_doacao: int) -> Optional[Doacao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_doacao,))
        row = cursor.fetchone()
        if row:
            # Tentar parse com hora, se falhar tentar apenas data
            try:
                data_hora = datetime.strptime(row["data_hora"], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    data_hora = datetime.strptime(row["data_hora"], '%Y-%m-%d')
                except ValueError:
                    data_hora = None
            
            return Doacao(
                cod_doacao=row["cod_doacao"],
                cod_doador=row["cod_doador"],
                cod_agendamento=row["cod_agendamento"],
                data_hora=data_hora,
                quantidade=row["quantidade"],
                status=row["status"],
                observacoes=row["observacoes"]
            )
        return None
    
def update(doacao: Doacao) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                doacao.cod_doador,
                doacao.cod_agendamento,
                doacao.data_hora,
                doacao.quantidade,
                doacao.status,
                doacao.observacoes,
                doacao.cod_doacao
            ),
        )
        return cursor.rowcount > 0

def delete(cod_doacao: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_doacao,))
        return cursor.rowcount > 0

def obter_doacoes_completas_por_doador(cod_doador: int) -> list[dict]:
    """
    Retorna lista de doações com informações completas (doador, unidade, endereço)
    para um doador específico
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_DOACOES_COMPLETAS_POR_DOADOR, (cod_doador,))
        rows = cursor.fetchall()
        doacoes = []
        for row in rows:
            # Tentar converter data_hora com diferentes formatos
            data_hora_obj = None
            if row['data_hora']:
                try:
                    # Tenta formato completo com hora
                    data_hora_obj = datetime.strptime(row['data_hora'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    try:
                        # Tenta formato apenas com data
                        data_hora_obj = datetime.strptime(row['data_hora'], '%Y-%m-%d')
                    except ValueError:
                        # Se falhar, deixa None
                        data_hora_obj = None
            
            doacao = {
                'cod_doacao': row['cod_doacao'],
                'cod_doador': row['cod_doador'],
                'cod_agendamento': row['cod_agendamento'],
                'data_hora': data_hora_obj,
                'quantidade': row['quantidade'],
                'status': row['status'],
                'nome_doador': row['nome_doador'],
                'tipo_sanguineo': row['tipo_sanguineo'],
                'fator_rh': row['fator_rh'],
                'tipo_sanguineo_completo': f"{row['tipo_sanguineo']}{row['fator_rh']}" if row['tipo_sanguineo'] and row['fator_rh'] else None,
                'nome_unidade': row['nome_unidade'],
                'rua_unidade': row['rua_unidade'],
                'bairro_unidade': row['bairro_unidade'],
                'cep_unidade': row['cep_unidade'],
                'telefone_unidade': row['telefone_unidade'],
                'nome_cidade': row['nome_cidade'],
                'sigla_estado': row['sigla_estado'],
                'endereco_completo': f"{row['rua_unidade']} - {row['bairro_unidade']}" if row['rua_unidade'] and row['bairro_unidade'] else None,
                'observacoes': row['observacoes']
            }
            doacoes.append(doacao)
        return doacoes

def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)
