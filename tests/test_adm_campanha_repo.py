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
    