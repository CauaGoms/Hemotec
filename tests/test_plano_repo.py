import sys
import os
from data.repo.plano_repo import *

class TestPlanoRepo:
    def test_criar_tabela_plano(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"