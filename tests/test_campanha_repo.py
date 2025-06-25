import sys
import os
from data.repo.campanha_repo import *

class TestCampanhaRepo:
    def test_criar_tabela_campanha(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"