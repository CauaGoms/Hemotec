import sys
import os
from data.repo.adm_campanha_repo import *

class TestAdmCampanhaRepo:
    def test_criar_tabela_adm_campanha(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

# def test_inserir_adm_campanha(self, test_db):
#         #Arrange
#         criar_tabela()
#         adm_campanha_teste = Adm_campanha(0, 0, "papel teste")
#         #Act
#         id_adm_campanha_inserida = inserir(adm_campanha_teste)
#         #Assert
#         adm_campanha_db = obter_por_id(id_adm_campanha_inserida)
#         assert adm_campanha_db is not None, "A Adm da Campanha inserida não deveria ser None"
#         assert adm_campanha_db.cod_adm == 1, "O ID da Adm Campanha inserida deveria ser igual a 1"
#         assert adm_campanha_db.cod_campanha == "Cidade teste", "O nome da cidade inserida não confere"
#         assert adm_campanha_db.sigla_estado == "sigla teste", "A sigla do estado inserida não confere"