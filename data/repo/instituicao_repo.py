from typing import Optional
from data.model.instituicao_model import Instituicao
from data.sql.instituicao_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0
    

def inserir(instituicao: Instituicao) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            instituicao.cnpj,
            instituicao.cod_gestor,
            instituicao.cod_assinatura,
            instituicao.nome,
            instituicao.email,
            instituicao.rua_instituicao,
            instituicao.bairro_instituicao,
            instituicao.cidade_instituicao,
            instituicao.cep_instituicao))
        return cursor.lastrowid
    

def obter_todos() -> list[Instituicao]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        instituicao = [
            Instituicao(
                cnpj=row["cnpj"],
                cod_gestor=row["cod_gestor"],
                cod_assinatura=row["cod_assinatura"],
                nome=row["nome"],
                email=row["email"],
                rua_instituicao=row["rua_instituicao"],
                bairro_instituicao=row["bairro_instituicao"],
                cidade_instituicao=row["cidade_instituicao"],
                cep_instituicao=row["cep_instituicao"])  
                for row in rows]
        return instituicao
    
def obter_por_id(self, cod_instituicao: int) -> Optional[Instituicao]:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (cod_instituicao,))
        row = cursor.fetchone()
        if row:
            return Instituicao(
                cnpj=row["cnpj"],
                cod_gestor=row["cod_gestor"],
                cod_assinatura=row["cod_assinatura"],
                nome=row["nome"],
                email=row["email"],
                rua_instituicao=row["rua_instituicao"],
                bairro_instituicao=row["bairro_instituicao"],
                cidade_instituicao=row["cidade_instituicao"],
                cep_instituicao=row["cep_instituicao"]
            )
        return None
    
def update(self, instituicao: Instituicao) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            UPDATE,
            (
                instituicao.cnpj,
                instituicao.cod_gestor,
                instituicao.cod_assinatura,
                instituicao.nome,
                instituicao.email,
                instituicao.rua_instituicao,
                instituicao.bairro_instituicao,
                instituicao.cidade_instituicao,
                instituicao.cep_instituicao
            ),
        )
        return cursor.rowcount > 0

def delete(self, cod_instituicao: int) -> bool:
    with self._connect() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETE, (cod_instituicao,))
        return cursor.rowcount > 0