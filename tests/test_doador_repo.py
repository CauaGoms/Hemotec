import sys
import os
from data.repo.doador_repo import *

class TestDoadorRepo:
    def test_criar_tabela_doador(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"