import sys
import os
from data.repo.unidade_coleta_repo import *

class TestUnidadeColetaRepo:
    def test_criar_tabela_unidade_coleta(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"