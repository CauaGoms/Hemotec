import sys
import os
from data.repo.campanha_repo import *

class TestCampanhaRepo:
    def test_criar_tabela_campanha(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_campanha(self, test_db):
        #Arrange
        criar_tabela()
        campanha_teste = Campanha(0, "Campanha teste", "Descrição da campanha teste", "2023-01-01", "2023-12-31", "Ativa")
        #Act
        id_campanha_inserida = inserir(campanha_teste)
        #Assert
        campanha_db = obter_por_id(id_campanha_inserida)
        assert campanha_db is not None, "A Campanha inserida não deveria ser None"
        assert campanha_db.cod_campanha == 1, "O ID da Campanha inserida deveria ser igual a 1"
        assert campanha_db.titulo == "Campanha teste", "O título da campanha inserida não confere"
        assert campanha_db.descricao == "Descrição da campanha teste", "A descrição da campanha inserida não confere"
        assert campanha_db.data_inicio == "2023-01-01", "A data de início da campanha inserida não confere"
        assert campanha_db.data_fim == "2023-12-31", "A data de fim da campanha inserida não confere"
        assert campanha_db.status == "Ativa", "O status da campanha inserida não confere"