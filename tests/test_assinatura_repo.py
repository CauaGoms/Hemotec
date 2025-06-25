import sys
import os
from data.repo.assinatura_repo import *

class TestAssinaturaRepo:
    def test_criar_tabela_assinatura(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"