from data.repo.plano_repo import *

class TestPlanoRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, plano_exemplo):
        #Arrange
        criar_tabela()
        #Act
        id_tabela_inserida = inserir(plano_exemplo)
        #Assert
        dados_db = obter_por_id(plano_exemplo.cod_plano)
        assert dados_db is not None, "O Plano inserido não deveria ser None"
        assert dados_db.qtd_licenca == 10, "A qtd_licenca do plano inserido não confere"
        assert dados_db.nome == "nome teste", "O nome do plano inserido não confere"
        assert dados_db.valor == 10.0, "O valor do plano inserido não confere"
        assert dados_db.validade == 10, "A validade do plano inserido não confere"

    def test_update_existente(self, test_db, plano_exemplo):
        #Arrange
        criar_tabela()
        id_tabela_inserida = inserir(plano_exemplo)
        tabela_inserida = obter_por_id(id_tabela_inserida)
        #Act
        tabela_inserida.qtd_licenca = 10
        tabela_inserida.nome = "nome atualizado"
        tabela_inserida.valor = 10.0
        tabela_inserida.validade = 10
        resultado = update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da campanha deveria retornar True"
        dados_db = obter_por_id(id_tabela_inserida)
        assert dados_db.qtd_licenca == 10, "A qtd_licenca atualizada não confere"
        assert dados_db.nome == "nome atualizado", "O nome atualizado não confere"
        assert dados_db.valor == 10.0, "A valor atualizado não confere"
        assert dados_db.validade == 10, "A validade atualizada não confere"


    def test_update_inexistente(self, test_db, plano_exemplo):
        #Arrange
        criar_tabela()
        plano_exemplo.cod_plano = 999  # ID inexistente
        #Act
        resultado = update(plano_exemplo)
        #Assert
        assert resultado == False, "A atualização de um plano inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, plano_exemplo):
        #Arrange
        criar_tabela()
        id_tabela_inserida = inserir(plano_exemplo)
        #Act
        resultado = delete(id_tabela_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_exculida = obter_por_id(id_tabela_inserida)
        assert tabela_exculida is None, "O plano não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        criar_tabela()
        #Act
        resultado = delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de um plano inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_planos_exemplo):
        #Arrange
        criar_tabela()
        for campanha in lista_planos_exemplo:
            inserir(campanha)
        #Act
        dados_db = obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 campanhas"
        for i, campanha in enumerate(dados_db):
            assert campanha.cod_plano == i + 1, f"O ID do plano {i+1} não confere"
            assert campanha.qtd_licenca == (i + 1)*10, f"A qtd_licenca {i+1} não confere"
            assert campanha.nome == f'nome {i+1:02d}', f"O nome {i+1} não confere"
            assert campanha.valor== float((i+1) * 10), f"O valor {i+1} não confere"
            assert campanha.validade == (i+1) * 10, f"A validade {i+1} não confere"
        
    def test_obter_todos_vazia(self, test_db):
        #Arrange
        criar_tabela()
        #Act
        dados_db = obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia"

    def test_obter_por_id_existente(self, test_db, plano_exemplo):
        #Arrange
        criar_tabela()
        id_tabela_inserida = inserir(plano_exemplo)
        #Act
        dados_db = obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "A campanha obtida não deveria ser None"
        assert dados_db.cod_plano == id_tabela_inserida, "O ID do plano obtido deveria ser igual ao ID do plano inserido"
        assert dados_db.qtd_licenca== 10, "A qtd_licenca obtido deveria ser igual ao título inserido"
        assert dados_db.nome == "nome teste", "O nome obtido deveria ser igual a descrição da campanha inserida"
        assert dados_db.valor == 10.0, "O valor obtido deveria ser igual a data de início da campanha inserida"
        assert dados_db.validade == 10, "A validade de fim obtida deveria ser igual a data de fim da campanha inserida"


    def test_obter_por_id_inexistente(self, test_db):
        #Arrange
        criar_tabela()
        #Act
        dados_db = obter_por_id(999)
        #Assert
        assert dados_db is None, "O plano obtida deveria ser None para um ID inexistente"