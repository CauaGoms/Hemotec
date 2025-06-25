import sys
import os
from data.repo.notificacao_repo import *

class TestNotificacaoRepo:
    def test_criar_tabela_notificacao(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"