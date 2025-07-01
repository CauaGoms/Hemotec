import sys
import os
from data.repo import adm_campanha_repo, adm_unidade_repo, campanha_repo, usuario_repo
from data.repo.adm_campanha_repo import *
from data.util.database import get_connection

class TestAdmCampanhaRepo:
    def test_criar_tabela_adm_campanha(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

def test_inserir_adm_campanha(self, test_db, adm_campanha_exemplo, adm_unidade_exemplo, campanha_exemplo, usuario_exemplo):
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario_repo.criar_tabela()
        usuario_repo.inserir(usuario_exemplo, cursor)

        adm_unidade_repo.criar_tabela()
        adm_unidade_repo.inserir(adm_unidade_exemplo, cursor)

        campanha_repo.criar_tabela()
        campanha_repo.inserir(campanha_exemplo, cursor)

        adm_campanha_repo.criar_tabela()
        conn.commit()

    #Act
    id_tabela_inserida = adm_campanha_repo.inserir(adm_unidade_exemplo)      
    #Assert
    dados_db = adm_campanha_repo.obter_por_id(id_tabela_inserida)
    assert dados_db is not None, "A Adm da Campanha inserida não deveria ser None"
    assert dados_db.cod_adm == 1, "O ID da Adm Campanha inserida não confere"
    assert dados_db.cod_campanha == 1, "O ID da Campanha inserida não confere"
    assert dados_db.papel == "papel teste", "O papel inserido não confere"