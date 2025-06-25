import sys
import os
from data.repo.instituicao_repo import *

class TestInstituicaoRepo:
    def test_criar_tabela_instituicao(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"