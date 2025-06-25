import sys
import os
from data.repo.cidade_repo import *
from data.model.cidade_model import Cidade

class TestCidadeRepo:
    def test_criar_tabela_cidade(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"
    
    def test_inserir_cidade(self, test_db):
        #Arrange
        criar_tabela()
        cidade_teste = Cidade(0, "Cidade teste", "sigla teste")
        #Act
        id_cidade_inserida = inserir(cidade_teste)
        #Assert
        cidade_db = obter_por_id(id_cidade_inserida)
        assert cidade_db is not None, "A Cidade inserida não deveria ser None"
        assert cidade_db.cod_cidade == 1, "O ID da Cidade inserida deveria ser igual a 1"
        assert cidade_db.nome_cidade == "Cidade teste", "O nome da cidade inserida não confere"
        assert cidade_db.sigla_estado == "sigla teste", "A sigla do estado inserida não confere"

    def test_update_cidade(self, test_db):
        #Arrange
        criar_tabela()
        cidade_teste = Cidade(0, "Cidade teste", "sigla teste")
        id_cidade_inserida = inserir(cidade_teste)
        cidade_inserida = obter_por_id(id_cidade_inserida)
        #Act
        cidade_inserida.nome_cidade = "Cidade atualizada"
        cidade_inserida.sigla_estado = "sigla atualizada"
        resultado = update(cidade_inserida)
        #Assert
        assert resultado == True, "A atualização da cidade deveria retornar True"
        cidade_db = obter_por_id(id_cidade_inserida)
        assert cidade_db.nome_cidade == "Cidade atualizada", "O nome da cidade atualizada não confere"
        assert cidade_db.sigla_estado == "sigla atualizada", "A sigla do estado atualizada não confere"
        
