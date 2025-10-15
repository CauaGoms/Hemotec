import os
from sqlite3 import Connection
from typing import Optional
from data.model.prontuario_model import Prontuario
from data.sql.prontuario_sql import *
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
    

def inserir(prontuario: Prontuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            prontuario.cod_doacao,
            prontuario.data_criacao,
            prontuario.data_atualizacao,
            prontuario.jejum,
            prontuario.diabetes,
            prontuario.hipertensao,
            prontuario.cardiopatia,
            prontuario.cancer,
            prontuario.hepatite,
            prontuario.outros,
            prontuario.detalhes_outros,
            prontuario.sintomas_gripais,
            prontuario.medicamentos,
            prontuario.detalhes_medicamentos,
            prontuario.fumante,
            prontuario.alcool,
            prontuario.droga,
            prontuario.ist,
            prontuario.atividade,
            prontuario.sono,
            prontuario.tatuagem_e_outros
            ))
        return cursor.lastrowid
    

def obter_todos() -> list[Prontuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        prontuario = [
            Prontuario(
                cod_prontuario=row["cod_prontuario"],
                cod_doacao=row["cod_doacao"],
                data_criacao=datetime.strptime(row["data_criacao"], '%Y-%m-%d'),
                data_atualizacao=datetime.strptime(row["data_atualizacao"], '%Y-%m-%d'),
                jejum=row["jejum"],
                diabetes=row["diabetes"],
                hipertensao=row["hipertensao"],
                cardiopatia=row["cardiopatia"],
                cancer=row["cancer"],
                hepatite=row["hepatite"],
                outros=row["outros"],
                detalhes_outros=row["detalhes_outros"],
                sintomas_gripais=row["sintomas_gripais"],
                medicamentos=row["medicamentos"],
                detalhes_medicamentos=row["detalhes_medicamentos"],
                fumante=row["fumante"],
                alcool=row["alcool"],
                droga=row["droga"],
                ist=row["ist"],
                atividade=row["atividade"],
                sono=row["sono"],
                tatuagem_e_outros=row["tatuagem_e_outros"]
                )  
                for row in rows]
        return prontuario
    
def obter_por_id(cod_prontuario: int) -> Optional[Prontuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_prontuario,))
        row = cursor.fetchone()
        if row:
            return Prontuario(
                cod_prontuario=row["cod_prontuario"],
                cod_doacao=row["cod_doacao"],
                data_criacao=datetime.strptime(row["data_criacao"], '%Y-%m-%d'),
                data_atualizacao=datetime.strptime(row["data_atualizacao"], '%Y-%m-%d'),
                jejum=row["jejum"],
                diabetes=row["diabetes"],
                hipertensao=row["hipertensao"],
                cardiopatia=row["cardiopatia"],
                cancer=row["cancer"],
                hepatite=row["hepatite"],
                outros=row["outros"],
                detalhes_outros=row["detalhes_outros"],
                sintomas_gripais=row["sintomas_gripais"],
                medicamentos=row["medicamentos"],
                detalhes_medicamentos=row["detalhes_medicamentos"],
                fumante=row["fumante"],
                alcool=row["alcool"],
                droga=row["droga"],
                ist=row["ist"],
                atividade=row["atividade"],
                sono=row["sono"],
                tatuagem_e_outros=row["tatuagem_e_outros"]
            )
        return None
    
def obter_por_doacao(cod_doacao: int) -> Optional[Prontuario]:
    """
    Obtém o prontuário relacionado a uma doação específica
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_DOACAO, (cod_doacao,))
        row = cursor.fetchone()
        if row:
            return Prontuario(
                cod_prontuario=row["cod_prontuario"],
                cod_doacao=row["cod_doacao"],
                data_criacao=datetime.strptime(row["data_criacao"], '%Y-%m-%d'),
                data_atualizacao=datetime.strptime(row["data_atualizacao"], '%Y-%m-%d'),
                jejum=row["jejum"],
                diabetes=row["diabetes"],
                hipertensao=row["hipertensao"],
                cardiopatia=row["cardiopatia"],
                cancer=row["cancer"],
                hepatite=row["hepatite"],
                outros=row["outros"],
                detalhes_outros=row["detalhes_outros"],
                sintomas_gripais=row["sintomas_gripais"],
                medicamentos=row["medicamentos"],
                detalhes_medicamentos=row["detalhes_medicamentos"],
                fumante=row["fumante"],
                alcool=row["alcool"],
                droga=row["droga"],
                ist=row["ist"],
                atividade=row["atividade"],
                sono=row["sono"],
                tatuagem_e_outros=row["tatuagem_e_outros"]
            )
        return None
    
def obter_por_doador(cod_doador: int) -> Optional[Prontuario]:
    """
    Obtém o prontuário mais recente de um doador
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        # Busca o prontuário da doação mais recente do doador
        cursor.execute("""
            SELECT p.cod_prontuario, p.cod_doacao, p.data_criacao, p.data_atualizacao, 
                   p.jejum, p.diabetes, p.hipertensao, p.cardiopatia, p.cancer, p.hepatite, 
                   p.outros, p.detalhes_outros, p.sintomas_gripais, p.medicamentos, 
                   p.detalhes_medicamentos, p.fumante, p.alcool, p.droga, p.ist, 
                   p.atividade, p.sono, p.tatuagem_e_outros
            FROM prontuario p
            INNER JOIN doacao d ON p.cod_doacao = d.cod_doacao
            WHERE d.cod_doador = ?
            ORDER BY p.data_criacao DESC
            LIMIT 1
        """, (cod_doador,))
        row = cursor.fetchone()
        if row:
            return Prontuario(
                cod_prontuario=row["cod_prontuario"],
                cod_doacao=row["cod_doacao"],
                data_criacao=datetime.strptime(row["data_criacao"], '%Y-%m-%d') if isinstance(row["data_criacao"], str) else row["data_criacao"],
                data_atualizacao=datetime.strptime(row["data_atualizacao"], '%Y-%m-%d') if isinstance(row["data_atualizacao"], str) else row["data_atualizacao"],
                jejum=row["jejum"],
                diabetes=row["diabetes"],
                hipertensao=row["hipertensao"],
                cardiopatia=row["cardiopatia"],
                cancer=row["cancer"],
                hepatite=row["hepatite"],
                outros=row["outros"],
                detalhes_outros=row["detalhes_outros"],
                sintomas_gripais=row["sintomas_gripais"],
                medicamentos=row["medicamentos"],
                detalhes_medicamentos=row["detalhes_medicamentos"],
                fumante=row["fumante"],
                alcool=row["alcool"],
                droga=row["droga"],
                ist=row["ist"],
                atividade=row["atividade"],
                sono=row["sono"],
                tatuagem_e_outros=row["tatuagem_e_outros"]
            )
        return None

def update(prontuario: Prontuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                prontuario.cod_doacao,
                prontuario.data_criacao,
                prontuario.data_atualizacao,
                prontuario.jejum,
                prontuario.diabetes,
                prontuario.hipertensao,
                prontuario.cardiopatia,
                prontuario.cancer,
                prontuario.hepatite,
                prontuario.outros,
                prontuario.detalhes_outros,
                prontuario.sintomas_gripais,
                prontuario.medicamentos,
                prontuario.detalhes_medicamentos,
                prontuario.fumante,
                prontuario.alcool,
                prontuario.droga,
                prontuario.ist,
                prontuario.atividade,
                prontuario.sono,
                prontuario.tatuagem_e_outros
            ),
        )
        return cursor.rowcount > 0

def delete(cod_prontuario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_prontuario,))
        return cursor.rowcount > 0

def inserir_dados_iniciais(conexao: Connection) -> None:
    lista = obter_todos()
    if lista: 
        return
    caminho_arquivo_sql = os.path.join(os.path.dirname(__file__), '../data/insert_categorias.sql')
    with open(caminho_arquivo_sql, 'r', encoding='utf-8') as arquivo:
        sql_inserts = arquivo.read()
        conexao.execute(sql_inserts)