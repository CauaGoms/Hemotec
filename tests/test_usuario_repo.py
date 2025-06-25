import sys
import os
from data.repo.usuario_repo import *

class TestUsuarioRepo:
    def test_criar_tabela_usuario(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"