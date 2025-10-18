import os
from sqlite3 import Connection
from typing import Optional
from data.model.agendamento_model import Agendamento
from data.sql.agendamento_sql import *
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
    

def inserir(agendamento: Agendamento) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            agendamento.cod_colaborador,
            agendamento.cod_doador,
            agendamento.data_hora,
            agendamento.status,
            agendamento.tipo_agendamento,
            agendamento.local_agendamento
        ))
        return cursor.lastrowid
    

def obter_todos() -> list[Agendamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        agendamento = []
        for row in rows:
            # Tentar parse com hora, se falhar tentar apenas data
            try:
                data_hora = datetime.strptime(row["data_hora"], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    data_hora = datetime.strptime(row["data_hora"], '%Y-%m-%d')
                except ValueError:
                    data_hora = None
            
            agendamento.append(Agendamento(
                cod_agendamento=row["cod_agendamento"],
                cod_colaborador=row["cod_colaborador"],
                cod_doador=row["cod_doador"],
                data_hora=data_hora,
                status=row["status"],
                tipo_agendamento=row["tipo_agendamento"],
                local_agendamento=row["local_agendamento"]
            ))
        return agendamento
    
def obter_por_id(cod_agendamento: int) -> Optional[Agendamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_agendamento,))
        row = cursor.fetchone()
        if row:
            # Debug: imprimir valor da data_hora do banco
            print(f"DEBUG - data_hora do banco: '{row['data_hora']}' (tipo: {type(row['data_hora'])})")
            
            # Tentar parse com hora, se falhar tentar apenas data
            try:
                data_hora = datetime.strptime(row["data_hora"], '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                print(f"DEBUG - Erro ao fazer parse com hora: {e}")
                try:
                    data_hora = datetime.strptime(row["data_hora"], '%Y-%m-%d')
                except ValueError as e2:
                    print(f"DEBUG - Erro ao fazer parse só data: {e2}")
                    data_hora = None
            
            print(f"DEBUG - data_hora após parse: {data_hora}")
            
            return Agendamento(
                cod_agendamento=row["cod_agendamento"],
                cod_colaborador=row["cod_colaborador"],
                cod_doador=row["cod_doador"],
                data_hora=data_hora,
                status=row["status"],
                tipo_agendamento=row["tipo_agendamento"],
                local_agendamento=row["local_agendamento"]
            )
        return None
    
def update(agendamento: Agendamento) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                agendamento.data_hora,
                agendamento.status,
                agendamento.tipo_agendamento,
                agendamento.cod_agendamento
            ),
        )
        return cursor.rowcount > 0

def delete(cod_agendamento: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_agendamento,))
        return cursor.rowcount > 0
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)