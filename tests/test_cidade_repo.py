from data.repo.cidade_repo import *

class TestCidadeRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"
    
    def test_inserir(self, test_db, cidade_exemplo):
        #Arrange
        criar_tabela()
        #Act
        id_tabela_inserida = inserir(cidade_exemplo)
        #Assert
        dados_db = obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "A Cidade inserida não deveria ser None"
        assert dados_db.cod_cidade == 1, "O ID da Cidade inserida deveria ser igual a 1"
        assert dados_db.nome_cidade == "nome_cidade teste", "O nome da cidade inserida não confere"
        assert dados_db.sigla_estado == "sigla_estado teste", "A sigla do estado inserida não confere"

    def test_update_existente(self, test_db, cidade_exemplo):
        #Arrange
        criar_tabela()
        id_tabela_inserida = inserir(cidade_exemplo)
        tabela_inserida = obter_por_id(id_tabela_inserida)
        #Act
        tabela_inserida.nome_cidade = "nome_cidade atualizada"
        tabela_inserida.sigla_estado = "sigla_estado atualizada"
        resultado = update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da cidade deveria retornar True"
        dados_db = obter_por_id(id_tabela_inserida)
        assert dados_db.nome_cidade == "nome_cidade atualizada", "O nome da cidade atualizada não confere"
        assert dados_db.sigla_estado == "sigla_estado atualizada", "A sigla do estado atualizada não confere"

    def test_update_inexistente(self, test_db, cidade_exemplo):
        #Arrange
        criar_tabela()
        cidade_exemplo.cod_cidade = 999  # ID inexistente
        #Act
        resultado = update(cidade_exemplo)
        #Assert
        assert resultado == False, "A atualização de uma cidade inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, cidade_exemplo):
        #Arrange
        criar_tabela()
        id_tabela_inserida = inserir(cidade_exemplo)
        #Act
        resultado = delete(id_tabela_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_exculida = obter_por_id(id_tabela_inserida)
        assert tabela_exculida is None, "A cidade não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        criar_tabela()
        #Act
        resultado = delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma cidade inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_cidades_exemplo):
        #Arrange
        criar_tabela()
        for cidade in lista_cidades_exemplo:
            inserir(cidade)
        #Act
        dados_db = obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 cidades"
        for i, cidade in enumerate(dados_db):
            assert cidade.cod_cidade == i + 1, f"O ID da cidade {i+1} não confere"
            assert cidade.nome_cidade == f'nome_cidade {i+1:02d}', f"O nome da cidade {i+1} não confere"
            assert cidade.sigla_estado == f'sigla_estado {i+1:02d}', f"A sigla do estado da cidade {i+1} não confere"
        
    def test_obter_todos_vazia(self, test_db):
        #Arrange
        criar_tabela()
        #Act
        dados_db = obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo):
        #Arrange
        criar_tabela()
        id_tabela_inserida = inserir(cidade_exemplo)
        #Act
        dados_db = obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "A Cidade obtida não deveria ser None"
        assert dados_db.cod_cidade == id_tabela_inserida, "O ID da Cidade obtida deveria ser igual ao ID da cidade inserido"
        assert dados_db.nome_cidade == "nome_cidade teste", "O nome da Cidade obtida deveria ser igual ao nome da cidade inserido"
        assert dados_db.sigla_estado == "sigla_estado teste", "A sigla do estado obtida deveria ser igual a sigla do estado da cidade inserida"

    def test_obter_por_id_inexistente(self, test_db):
        #Arrange
        criar_tabela()
        #Act
        dados_db = obter_por_id(999)
        #Assert
        assert dados_db is None, "A Cidade obtida deveria ser None para um ID inexistente"