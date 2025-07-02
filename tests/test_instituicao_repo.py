from data.repo import instituicao_repo, cidade_repo
from data.model.instituicao_model import Instituicao


class TestInstituicaoRepo:
    def test_criar_tabela_instituicao(self, test_db):
        #Arrange
        #Act
        resultado = instituicao_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, instituicao_exemplo, cidade_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        id_cidade = cidade_repo.inserir(cidade_exemplo)

        instituicao_repo.criar_tabela()
        
        #Act
        id_tabela_inserida = instituicao_repo.inserir(instituicao_exemplo)
        #Assert
        dados_db = instituicao_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "A instituição inserida não deveria ser None"
        assert dados_db.cod_instituicao == id_tabela_inserida, "O ID da instituição inserida não confere"
        assert dados_db.cnpj == "cnpj teste", "O ID do usuário inserido deveria ser igual a 1"
        assert dados_db.nome == "nome teste", "O nome do usuário inserida não confere"
        assert dados_db.email == "email teste", "O email do usuário inserido não confere"
        assert dados_db.rua_instituicao == "rua_instituicao teste", "A sigla do estado inserida não confere"
        assert dados_db.bairro_instituicao == "bairro_instituicao teste", "O CPF do usuário inserido não confere"
        assert dados_db.cidade_instituicao == id_cidade, "A cidade_instituição da instituição inserida não confere"
        assert dados_db.cep_instituicao == "cep_instituicao teste", "A rua do usuário inserido não confere"
        assert dados_db.telefone == "telefone teste", "O telefone do usuário inserido não confere"


    def test_update_existente(self, test_db, instituicao_exemplo, cidade_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        instituicao_repo.criar_tabela()
        id_tabela_inserida = instituicao_repo.inserir(instituicao_exemplo)
        
        tabela_inserida = instituicao_repo.obter_por_id(id_tabela_inserida)
            
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.cnpj = "cnpj atualizado"
        tabela_inserida.nome = "nome atualizada"
        tabela_inserida.email = "email atualizada"
        tabela_inserida.rua_instituicao = "rua_instituicao atualizada"
        tabela_inserida.bairro_instituicao = "bairro_instituicao atualizado"
        tabela_inserida.cep_instituicao = "cep_instituicao atualizado"
        tabela_inserida.telefone = "telefone atualizado"
        resultado = instituicao_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização do usuário deveria retornar True"
        dados_db = instituicao_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.nome == "nome atualizada", "O nome da cidade atualizada não confere"
        assert dados_db.email == "email atualizada", "A sigla do estado atualizada não confere"
        assert dados_db.rua_instituicao == "rua_instituicao atualizada", "A senha do usuário atualizado não confere"
        assert dados_db.bairro_instituicao == "bairro_instituicao atualizado", "O CPF do usuário atualizado não confere"
        assert dados_db.cep_instituicao == "cep_instituicao atualizado", "O status do usuário atualizado não confere"
        assert dados_db.telefone == "telefone atualizado", "O telefone do usuário atualizado não confere"

    def test_update_inexistente(self, test_db, instituicao_exemplo, cidade_exemplo):
        #Arrange
        #Não é necessário inserir as tabelas anteriores        
        instituicao_repo.criar_tabela()
        instituicao_exemplo.cod_instituição = 999  # ID inexistente
        #Act
        resultado = instituicao_repo.update(instituicao_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, instituicao_exemplo, cidade_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        instituicao_repo.criar_tabela()
        id_tabela_inserida = instituicao_repo.inserir(instituicao_exemplo)
                   
        #Act
        resultado = instituicao_repo.delete(id_tabela_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = instituicao_repo.obter_por_id(id_tabela_inserida)
        assert tabela_excluida is None, "A instituição não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        instituicao_repo.criar_tabela()
        #Act
        resultado = instituicao_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma instituição inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_instituicoes_exemplo, lista_cidades_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        for cidade in lista_cidades_exemplo:
            cidade_repo.inserir(cidade)
        
        
        instituicao_repo.criar_tabela()
        for instituicao in lista_instituicoes_exemplo:
            instituicao_repo.inserir(instituicao)
            
        #Act
        dados_db = instituicao_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 cidades"
        assert all(isinstance(i, Instituicao) for i in dados_db), "Todos os itens retornados deveriam ser do tipo Usuario"
        cod_esperados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        cod_retornados = [i.cod_instituicao for i in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs dos usuários retornados deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        for cidade in lista_cidades_exemplo:
            cidade_repo.inserir(cidade)

        instituicao_repo.criar_tabela()
        #Act
        dados_db = instituicao_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, instituicao_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        instituicao_repo.criar_tabela()
        id_tabela_inserida = instituicao_repo.inserir(instituicao_exemplo)
           
        #Act
        dados_db = instituicao_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "A Cidade obtida não deveria ser None"
        assert dados_db.cod_instituicao == id_tabela_inserida, "O ID da instituição obtida deveria ser igual ao ID da cidade inserido"
        assert dados_db.nome == "nome teste", "O nome da instituição obtida deveria ser igual ao nome da cidade inserido"
        assert dados_db.email == "email teste", "O email da instituição obtida deveria ser igual ao email da cidade inserido"
        assert dados_db.rua_instituicao == "rua_instituicao teste", "A rua da instituição obtida deveria ser igual a rua da cidade inserida"
        assert dados_db.bairro_instituicao == "bairro_instituicao teste", "O bairro da instituição obtida deveria ser igual ao bairro da cidade inserida"
        assert dados_db.cidade_instituicao == 1, "A cidade_instituição da instituição obtida deveria ser igual a 1"
        assert dados_db.cep_instituicao == "cep_instituicao teste", "O cep da instituição obtida deveria ser igual ao cep da cidade inserida"
        assert dados_db.telefone == "telefone teste", "O telefone do usuário obtida deveria ser igual ao telefone do usuário inserido"

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)
        instituicao_repo.criar_tabela()
        #Act
        dados_db = instituicao_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A Cidade obtida deveria ser None para um ID inexistente"