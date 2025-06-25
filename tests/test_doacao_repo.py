import sys
import os
from data.repo.doacao_repo import *

class TestDoacaoRepo:
    def test_criar_tabela_doacao(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"