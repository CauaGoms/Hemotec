import sys
import os
from data.repo.exame_repo import *

class TestExameRepo:
    def test_criar_tabela_exame(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"