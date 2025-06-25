import sys
import os
from data.repo.prontuario_repo import *

class TestProntuarioRepo:
    def test_criar_tabela_prontuario(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"