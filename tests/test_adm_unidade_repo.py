import sys
import os
from data.repo.adm_unidade_repo import *

class TestAdmUnidadeRepo:
    def test_criar_tabela_adm_unidade(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"