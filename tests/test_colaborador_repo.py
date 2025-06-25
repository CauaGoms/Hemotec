import sys
import os
from data.repo.colaborador_repo import *

class TestColaboradorRepo:
    def test_criar_tabela_colaborador(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"