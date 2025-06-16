from typing import Optional
from data.model.assinatura_model import Assinatura
from data.sql.assinatura_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(assinatura: Assinatura) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            assinatura.cnpj,
            assinatura.cod_plano,
            assinatura.cod_licenca,
            assinatura.data_inicio,
            assinatura.data_fim,
            assinatura.valor,
            assinatura.qtd_licenca))
        return cursor.lastrowid
    

def obter_todos() -> list[Assinatura]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        assinatura = [
            Assinatura(
                cod_assinatura=row["cod_assinatura"],
                cnpj=row["cnpj"],
                cod_plano=row["cod_plano"],
                cod_licenca=row["cod_licenca"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                valor=row["valor"],
                qtd_licenca=row["qtd_licenca"]
                )  
                for row in rows]
        return assinatura
    
def obter_por_id(self, cod_assinatuta: int) -> Optional[Assinatura]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_assinatuta,))
        row = cursor.fetchone()
        if row:
            return Assinatura(
                cod_assinatura=row["cod_assinatura"],
                cnpj=row["cnpj"],
                cod_plano=row["cod_plano"],
                cod_licenca=row["cod_licenca"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                valor=row["valor"],
                qtd_licenca=row["qtd_licenca"]
            )
        return None
    
def update(self, assinatura: Assinatura) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                assinatura.cod_assinatura,
                assinatura.cnpj,
                assinatura.cod_plano,
                assinatura.cod_licenca,
                assinatura.data_inicio,
                assinatura.data_fim,
                assinatura.valor,
                assinatura.qtd_licenca
            ),
        )
        return cursor.rowcount > 0

def delete(self, cod_assinatura: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_assinatura,))
        return cursor.rowcount > 0