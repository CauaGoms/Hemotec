import os
from sqlite3 import Connection
from typing import Optional
from data.model.horario_funcionamento_model import Horario_funcionamento
from data.sql.horario_funcionamento_sql import *
from util.database import get_connection
from datetime import date, time, datetime

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela horario_funcionamento: {e}")
        return False
    

def inserir(horario_funcionamento: Horario_funcionamento) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            horario_funcionamento.horario_inicio,
            horario_funcionamento.horario_fim,
            horario_funcionamento.intervalo_doacoes,
            horario_funcionamento.data
        ))
        return cursor.lastrowid
    

def obter_todos() -> list[Horario_funcionamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        horarios = [
            Horario_funcionamento(
                cod_horario_funcionamento=row["cod_horario_funcionamento"],
                horario_inicio=datetime.strptime(row["horario_inicio"], '%H:%M:%S').time() if isinstance(row["horario_inicio"], str) else row["horario_inicio"],
                horario_fim=datetime.strptime(row["horario_fim"], '%H:%M:%S').time() if isinstance(row["horario_fim"], str) else row["horario_fim"],
                intervalo_doacoes=row["intervalo_doacoes"],
                data=datetime.strptime(row["data"], '%Y-%m-%d').date() if isinstance(row["data"], str) else row["data"]
            )
            for row in rows]
        return horarios
    
def obter_por_id(cod_horario_funcionamento: int) -> Optional[Horario_funcionamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_horario_funcionamento,))
        row = cursor.fetchone()
        if row:
            return Horario_funcionamento(
                cod_horario_funcionamento=row["cod_horario_funcionamento"],
                horario_inicio=datetime.strptime(row["horario_inicio"], '%H:%M:%S').time() if isinstance(row["horario_inicio"], str) else row["horario_inicio"],
                horario_fim=datetime.strptime(row["horario_fim"], '%H:%M:%S').time() if isinstance(row["horario_fim"], str) else row["horario_fim"],
                intervalo_doacoes=row["intervalo_doacoes"],
                data=datetime.strptime(row["data"], '%Y-%m-%d').date() if isinstance(row["data"], str) else row["data"]
            )
        return None

def obter_por_data(data: date) -> list[Horario_funcionamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_DATA, (data,))
        rows = cursor.fetchall()
        horarios = [
            Horario_funcionamento(
                cod_horario_funcionamento=row["cod_horario_funcionamento"],
                horario_inicio=datetime.strptime(row["horario_inicio"], '%H:%M:%S').time() if isinstance(row["horario_inicio"], str) else row["horario_inicio"],
                horario_fim=datetime.strptime(row["horario_fim"], '%H:%M:%S').time() if isinstance(row["horario_fim"], str) else row["horario_fim"],
                intervalo_doacoes=row["intervalo_doacoes"],
                data=datetime.strptime(row["data"], '%Y-%m-%d').date() if isinstance(row["data"], str) else row["data"]
            )
            for row in rows]
        return horarios

def obter_por_periodo(data_inicio: date, data_fim: date) -> list[Horario_funcionamento]:
    """
    Retorna os horários de funcionamento em um período específico
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PERIODO, (data_inicio, data_fim))
        rows = cursor.fetchall()
        horarios = [
            Horario_funcionamento(
                cod_horario_funcionamento=row["cod_horario_funcionamento"],
                horario_inicio=datetime.strptime(row["horario_inicio"], '%H:%M:%S').time() if isinstance(row["horario_inicio"], str) else row["horario_inicio"],
                horario_fim=datetime.strptime(row["horario_fim"], '%H:%M:%S').time() if isinstance(row["horario_fim"], str) else row["horario_fim"],
                intervalo_doacoes=row["intervalo_doacoes"],
                data=datetime.strptime(row["data"], '%Y-%m-%d').date() if isinstance(row["data"], str) else row["data"]
            )
            for row in rows]
        return horarios
    
def update(horario_funcionamento: Horario_funcionamento) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                horario_funcionamento.horario_inicio,
                horario_funcionamento.horario_fim,
                horario_funcionamento.intervalo_doacoes,
                horario_funcionamento.data,
                horario_funcionamento.cod_horario_funcionamento
            ),
        )
        return cursor.rowcount > 0

def delete(cod_horario_funcionamento: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_horario_funcionamento,))
        return cursor.rowcount > 0

def verificar_disponibilidade(data: date, horario_inicio: time, horario_fim: time) -> Optional[Horario_funcionamento]:
    """
    Verifica se existe um horário de funcionamento disponível
    em uma data e horário específicos
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_DISPONIBILIDADE, (data, horario_inicio, horario_fim))
        row = cursor.fetchone()
        if row:
            return Horario_funcionamento(
                cod_horario_funcionamento=row["cod_horario_funcionamento"],
                horario_inicio=datetime.strptime(row["horario_inicio"], '%H:%M:%S').time() if isinstance(row["horario_inicio"], str) else row["horario_inicio"],
                horario_fim=datetime.strptime(row["horario_fim"], '%H:%M:%S').time() if isinstance(row["horario_fim"], str) else row["horario_fim"],
                intervalo_doacoes=row["intervalo_doacoes"],
                data=datetime.strptime(row["data"], '%Y-%m-%d').date() if isinstance(row["data"], str) else row["data"]
            )
        return None

def calcular_vagas_disponiveis(horario_funcionamento: Horario_funcionamento) -> int:
    """
    Calcula quantas vagas de doação estão disponíveis em um horário de funcionamento
    baseado no horário de início, fim e intervalo entre doações
    """
    inicio = datetime.combine(date.today(), horario_funcionamento.horario_inicio)
    fim = datetime.combine(date.today(), horario_funcionamento.horario_fim)
    
    duracao_minutos = (fim - inicio).total_seconds() / 60
    
    # Calcula o número de vagas possíveis
    vagas = int(duracao_minutos / horario_funcionamento.intervalo_doacoes)
    
    return vagas

def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/inserts.sql')
    if os.path.exists(caminho_arquivo_sql):
        with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
            sql_inserts = arquivo.read()
            conexao.execute(sql_inserts)
