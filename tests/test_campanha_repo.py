from data.repo.campanha_repo import *

class TestCampanhaRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, campanha_exemplo):
        #Arrange
        criar_tabela()
        #Act
        id_tabela_inserida = inserir(campanha_exemplo)
        #Assert
        dados_db = obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "A Campanha inserida não deveria ser None"
        assert dados_db.cod_campanha == 1, "O ID da Campanha inserida deveria ser igual a 1"
        assert dados_db.titulo == "titulo teste", "O título da campanha inserida não confere"
        assert dados_db.descricao == "descricao teste", "A descrição da campanha inserida não confere"
        assert dados_db.data_inicio.strftime("%Y-%m-%d") == "2025-01-01", "A data de início da campanha inserida não confere"
        assert dados_db.data_fim.strftime("%Y-%m-%d") == "2025-01-01", "A data de fim da campanha inserida não confere"
        assert dados_db.status == "status teste", "O status da campanha inserida não confere"

    # def test_inserir(self, test_db, campanha_exemplo):
    #     #Arrange
    #     criar_tabela()
    #     #Act
    #     id_campanha_inserida = inserir(campanha_exemplo)
    #     #Assert
    #     campanha_db = obter_por_id(id_campanha_inserida)
    #     assert campanha_db is not None, "A Campanha inserida não deveria ser None"
    #     assert campanha_db.cod_campanha == 1, "O ID da Campanha inserida deveria ser igual a 1"
    #     assert campanha_db.titulo == "titulo teste", "O título da campanha inserida não confere"
    #     assert campanha_db.descricao == "descricao teste", "A descrição da campanha inserida não confere"
    #     assert campanha_db.data_inicio == "2025-01-01", "A data de início da campanha inserida não confere"
    #     assert campanha_db.data_fim == "2025-01-01", "A data de fim da campanha inserida não confere"
    #     assert campanha_db.status == "status teste", "O status da campanha inserida não confere"

    def test_update_existente(self, test_db, campanha_exemplo):
        #Arrange
        criar_tabela()
        id_tabela_inserida = inserir(campanha_exemplo)
        tabela_inserida = obter_por_id(id_tabela_inserida)
        #Act
        tabela_inserida.titulo = "titulo atualizada"
        tabela_inserida.descricao = "descricao atualizada"
        tabela_inserida.data_inicio = "2000-01-01"
        tabela_inserida.data_fim = "2000-01-01"
        tabela_inserida.status = "status atualizada"
        resultado = update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da campanha deveria retornar True"
        dados_db = obter_por_id(id_tabela_inserida)
        assert dados_db.titulo == "titulo atualizada", "O titulo atualizado não confere"
        assert dados_db.descricao == "descricao atualizada", "A descricao atualizada não confere"
        assert dados_db.data_inicio.strftime("%Y-%m-%d") == "2000-01-01", "A data de início atualizada não confere"
        assert dados_db.data_fim.strftime("%Y-%m-%d") == "2000-01-01", "A data de fim atualizada não confere"
        assert dados_db.status == "status atualizada", "O status atualizado não confere"


    def test_update_inexistente(self, test_db, campanha_exemplo):
        #Arrange
        criar_tabela()
        campanha_exemplo.cod_campanha = 999  # ID inexistente
        #Act
        resultado = update(campanha_exemplo)
        #Assert
        assert resultado == False, "A atualização de uma campanha inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, campanha_exemplo):
        #Arrange
        criar_tabela()
        id_tabela_inserida = inserir(campanha_exemplo)
        #Act
        resultado = delete(id_tabela_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_exculida = obter_por_id(id_tabela_inserida)
        assert tabela_exculida is None, "A campanha não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        criar_tabela()
        #Act
        resultado = delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma campanha inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_campanhas_exemplo):
        #Arrange
        criar_tabela()
        for campanha in lista_campanhas_exemplo:
            inserir(campanha)
        #Act
        dados_db = obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 campanhas"
        for i, campanha in enumerate(dados_db):
            assert campanha.cod_campanha == i + 1, f"O ID da campanha {i+1} não confere"
            assert campanha.titulo == f'titulo {i+1:02d}', f"O título {i+1} não confere"
            assert campanha.descricao == f'descricao {i+1:02d}', f"A descrição {i+1} não confere"
            assert campanha.data_inicio.strftime("%Y-%m-%d") == f"2025-01-{i+1:02d}", f"A data de início {i+1} não confere"
            assert campanha.data_fim.strftime("%Y-%m-%d") == f"2025-01-{i+1:02d}", f"A data de fim {i+1} não confere"
            assert campanha.status == f"status {i+1:02d}", f"O status {i+1} não confere"
        
    def test_obter_todos_vazia(self, test_db):
        #Arrange
        criar_tabela()
        #Act
        dados_db = obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia"

    def test_obter_por_id_existente(self, test_db, campanha_exemplo):
        #Arrange
        criar_tabela()
        id_tabela_inserida = inserir(campanha_exemplo)
        #Act
        dados_db = obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "A campanha obtida não deveria ser None"
        assert dados_db.cod_campanha == id_tabela_inserida, "O ID da campanha obtido deveria ser igual ao ID da campanha inserido"
        assert dados_db.titulo == "titulo teste", "O título obtido deveria ser igual ao título inserido"
        assert dados_db.descricao == "descricao teste", "A descrição obtida deveria ser igual a descrição da campanha inserida"
        assert dados_db.data_inicio.strftime("%Y-%m-%d") == "2025-01-01", "A data de início obtida deveria ser igual a data de início da campanha inserida"
        assert dados_db.data_fim.strftime("%Y-%m-%d") == "2025-01-01", "A data de fim obtida deveria ser igual a data de fim da campanha inserida"
        assert dados_db.status == "status teste", "O status obtido deveria ser igual ao status da campanha inserida"

    def test_obter_por_id_inexistente(self, test_db):
        #Arrange
        criar_tabela()
        #Act
        dados_db = obter_por_id(999)
        #Assert
        assert dados_db is None, "A Campanha obtida deveria ser None para um ID inexistente"