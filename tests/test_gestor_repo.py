import sys
import os
from data.repo.gestor_repo import *

class TestGestorRepo:
    def test_criar_tabela_gestor(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"