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