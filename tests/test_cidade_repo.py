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
        
    def test_delete_cidade(self, test_db):
        #Arrange
        criar_tabela()
        cidade_teste = Cidade(0, "Cidade teste", "sigla teste")
        id_cidade_inserida = inserir(cidade_teste)
        #Act
        resultado = delete(id_cidade_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        cidade_exculida = obter_por_id(id_cidade_inserida)
        assert cidade_exculida is None, "A cidade não foi excluída corretamente, deveria ser None"

    # def test_obter_todos_cidade(self, test_db):
    #     #Arrange
    #     criar_tabela()
    #     for i in range(10):
    #         cidade_teste = Cidade(0, f"Cidade {i+1}", f"sigla {i+1}")
    #         inserir(cidade_teste)
    #     #Act
    #     cidades_1 = obter_todos(1, 10)
    #     cidades_2 = obter_todos(2, 4)
    #     cidades_3 = obter_todos(3, 4)
    #     #Assert
    #     assert len(cidades_1) == 10, "A primeira consulta deveria retornar 10 cidades na primeira página"
    #     assert len(cidades_2) == 4, "A segunda consulta deveria retornar 4 cidades na segunda página"
    #     assert len(cidades_3) == 2, "A terceira consulta deveria retornar 2 cidades na terceira página"
    #     assert cidades_3[0].cod_cidade == 8, "A primeira cidade da terceira página deveria ter o ID 8"

    def test_obter_por_id_cidade(self, test_db):
        #Arrange
        criar_tabela()
        cidade_teste = Cidade(0, "Cidade teste", "sigla teste")
        id_cidade_inserida = inserir(cidade_teste)
        #Act
        cidade_db = obter_por_id(id_cidade_inserida)
        #Assert
        assert cidade_db is not None, "A Cidade obtida não deveria ser None"
        assert cidade_db.cod_cidade == id_cidade_inserida, "O ID da Cidade obtida deveria ser igual ao ID da cidade inserido"
        assert cidade_db.nome_cidade == "Cidade teste", "O nome da Cidade obtida deveria ser igual ao nome da cidade inserido"
        assert cidade_db.sigla_estado == "sigla teste", "A sigla do estado obtida deveria ser igual a sigla do estado da cidade inserida"
