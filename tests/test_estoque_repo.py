import sys
import os
from data.repo.estoque_repo import *

class TestEstoqueRepo:
    def test_criar_tabela_estoque(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"