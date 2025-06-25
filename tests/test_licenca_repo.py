import sys
import os
from data.repo.licenca_repo import *

class TestLicencaRepo:
    def test_criar_tabela_licenca(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"