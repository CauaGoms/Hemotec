import os
from sqlite3 import Connection
from typing import Optional
from data.model.prontuario_model import Prontuario
from data.sql.prontuario_sql import *
from data.util.database import get_connection

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
            prontuario.cod_doador,
            prontuario.data_criacao,
            prontuario.data_atualizacao,
            prontuario.diabetes,
            prontuario.hipertensao,
            prontuario.cardiopatia,
            prontuario.cancer,
            prontuario.nenhuma,
            prontuario.outros,
            prontuario.medicamentos,
            prontuario.fumante,
            prontuario.alcool,
            prontuario.atividade,
            prontuario.jejum,
            prontuario.sono,
            prontuario.bebida,
            prontuario.sintomas_gripais,
            prontuario.tatuagem,
            prontuario.termos,
            prontuario.alerta))
        return cursor.lastrowid
    

def obter_todos() -> list[Prontuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        prontuario = [
            Prontuario(
                cod_prontuario=row["cod_prontuario"],
                cod_doador=row["cod_doador"],
                data_criacao=row["data_criacao"],
                data_atualizacao=row["data_atualizacao"],
                diabetes=row["diabetes"],
                hipertensao=row["hipertensao"],
                cardiopatia=row["cardiopatia"],
                cancer=row["cancer"],
                nenhuma=row["nenhuma"],
                outros=row["outros"],
                medicamentos=row["medicamentos"],
                fumante=row["fumante"],
                alcool=row["alcool"],
                atividade=row["atividade"],
                jejum=row["jejum"],
                sono=row["sono"],
                bebida=row["bebida"],
                sintomas_gripais=row["sintomas_gripais"],
                tatuagem=row["tatuagem"],
                termos=row["termos"],
                alerta=row["alerta"])  
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
                cod_doador=row["cod_doador"],
                data_criacao=row["data_criacao"],
                data_atualizacao=row["data_atualizacao"],
                diabetes=row["diabetes"],
                hipertensao=row["hipertensao"],
                cardiopatia=row["cardiopatia"],
                cancer=row["cancer"],
                nenhuma=row["nenhuma"],
                outros=row["outros"],
                medicamentos=row["medicamentos"],
                fumante=row["fumante"],
                alcool=row["alcool"],
                atividade=row["atividade"],
                jejum=row["jejum"],
                sono=row["sono"],
                bebida=row["bebida"],
                sintomas_gripais=row["sintomas_gripais"],
                tatuagem=row["tatuagem"],
                termos=row["termos"],
                alerta=row["alerta"]
            )
        return None
    
def update(prontuario: Prontuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                prontuario.cod_doador,
                prontuario.data_criacao,
                prontuario.data_atualizacao,
                prontuario.diabetes,
                prontuario.hipertensao,
                prontuario.cardiopatia,
                prontuario.cancer,
                prontuario.nenhuma,
                prontuario.outros,
                prontuario.medicamentos,
                prontuario.fumante,
                prontuario.alcool,
                prontuario.atividade,
                prontuario.jejum,
                prontuario.sono,
                prontuario.bebida,
                prontuario.sintomas_gripais,
                prontuario.tatuagem,
                prontuario.termos,
                prontuario.alerta,
                prontuario.cod_prontuario
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