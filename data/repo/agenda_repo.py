import os
from sqlite3 import Connection
from typing import Optional
from data.model.agenda_model import Agenda
from data.sql.agenda_sql import *
from util.database import get_connection
from datetime import date, time, datetime

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela agenda: {e}")
        return False
    

def inserir(agenda: Agenda) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            agenda.cod_unidade,
            agenda.cod_agendamento,
            agenda.data_agenda,
            agenda.hora_agenda,
            agenda.vagas,
            agenda.quantidade_doadores
        ))
        return cursor.lastrowid
    

def obter_todos() -> list[Agenda]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        agendas = [
            Agenda(
                cod_agenda=row["cod_agenda"],
                cod_unidade=row["cod_unidade"],
                cod_agendamento=row["cod_agendamento"],
                data_agenda=datetime.strptime(row["data_agenda"], '%Y-%m-%d').date() if isinstance(row["data_agenda"], str) else row["data_agenda"],
                hora_agenda=datetime.strptime(row["hora_agenda"], '%H:%M:%S').time() if isinstance(row["hora_agenda"], str) else row["hora_agenda"],
                vagas=row["vagas"],
                quantidade_doadores=row["quantidade_doadores"]
            )
            for row in rows]
        return agendas
    
def obter_por_id(cod_agenda: int) -> Optional[Agenda]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_agenda,))
        row = cursor.fetchone()
        if row:
            return Agenda(
                cod_agenda=row["cod_agenda"],
                cod_unidade=row["cod_unidade"],
                cod_agendamento=row["cod_agendamento"],
                data_agenda=datetime.strptime(row["data_agenda"], '%Y-%m-%d').date() if isinstance(row["data_agenda"], str) else row["data_agenda"],
                hora_agenda=datetime.strptime(row["hora_agenda"], '%H:%M:%S').time() if isinstance(row["hora_agenda"], str) else row["hora_agenda"],
                vagas=row["vagas"],
                quantidade_doadores=row["quantidade_doadores"]
            )
        return None

def obter_por_unidade(cod_unidade: int) -> list[Agenda]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_UNIDADE, (cod_unidade,))
        rows = cursor.fetchall()
        agendas = [
            Agenda(
                cod_agenda=row["cod_agenda"],
                cod_unidade=row["cod_unidade"],
                cod_agendamento=row["cod_agendamento"],
                data_agenda=datetime.strptime(row["data_agenda"], '%Y-%m-%d').date() if isinstance(row["data_agenda"], str) else row["data_agenda"],
                hora_agenda=datetime.strptime(row["hora_agenda"], '%H:%M:%S').time() if isinstance(row["hora_agenda"], str) else row["hora_agenda"],
                vagas=row["vagas"],
                quantidade_doadores=row["quantidade_doadores"]
            )
            for row in rows]
        return agendas

def obter_por_data(data_agenda: date) -> list[Agenda]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_DATA, (data_agenda,))
        rows = cursor.fetchall()
        agendas = [
            Agenda(
                cod_agenda=row["cod_agenda"],
                cod_unidade=row["cod_unidade"],
                cod_agendamento=row["cod_agendamento"],
                data_agenda=datetime.strptime(row["data_agenda"], '%Y-%m-%d').date() if isinstance(row["data_agenda"], str) else row["data_agenda"],
                hora_agenda=datetime.strptime(row["hora_agenda"], '%H:%M:%S').time() if isinstance(row["hora_agenda"], str) else row["hora_agenda"],
                vagas=row["vagas"],
                quantidade_doadores=row["quantidade_doadores"]
            )
            for row in rows]
        return agendas

def obter_por_unidade_e_data(cod_unidade: int, data_agenda: date) -> list[Agenda]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_UNIDADE_E_DATA, (cod_unidade, data_agenda))
        rows = cursor.fetchall()
        agendas = [
            Agenda(
                cod_agenda=row["cod_agenda"],
                cod_unidade=row["cod_unidade"],
                cod_agendamento=row["cod_agendamento"],
                data_agenda=datetime.strptime(row["data_agenda"], '%Y-%m-%d').date() if isinstance(row["data_agenda"], str) else row["data_agenda"],
                hora_agenda=datetime.strptime(row["hora_agenda"], '%H:%M:%S').time() if isinstance(row["hora_agenda"], str) else row["hora_agenda"],
                vagas=row["vagas"],
                quantidade_doadores=row["quantidade_doadores"]
            )
            for row in rows]
        return agendas
    
def update(agenda: Agenda) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                agenda.cod_unidade,
                agenda.cod_agendamento,
                agenda.data_agenda,
                agenda.hora_agenda,
                agenda.vagas,
                agenda.quantidade_doadores,
                agenda.cod_agenda
            ),
        )
        return cursor.rowcount > 0

def delete(cod_agenda: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_agenda,))
        return cursor.rowcount > 0

def incrementar_doadores(cod_agenda: int) -> bool:
    """
    Incrementa o contador de doadores agendados
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INCREMENTAR_DOADORES, (cod_agenda,))
        return cursor.rowcount > 0

def decrementar_doadores(cod_agenda: int) -> bool:
    """
    Decrementa o contador de doadores agendados (não permite valores negativos)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DECREMENTAR_DOADORES, (cod_agenda,))
        return cursor.rowcount > 0

def obter_vagas_disponiveis(cod_agenda: int) -> Optional[int]:
    """
    Retorna o número de vagas disponíveis para uma agenda
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_VAGAS_DISPONIVEIS, (cod_agenda,))
        row = cursor.fetchone()
        if row:
            return row["vagas_disponiveis"]
        return None

def tem_vagas_disponiveis(cod_agenda: int) -> bool:
    """
    Verifica se ainda há vagas disponíveis na agenda
    """
    vagas = obter_vagas_disponiveis(cod_agenda)
    return vagas is not None and vagas > 0
    
def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/inserts.sql')
    if os.path.exists(caminho_arquivo_sql):
        with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
            sql_inserts = arquivo.read()
            conexao.execute(sql_inserts)
