import sys
import os
from data.repo.agendamento_repo import *

class TestAgendamentoRepo:
    def test_criar_tabela_agendamento(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"