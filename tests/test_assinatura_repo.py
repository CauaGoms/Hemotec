from data.repo import cidade_repo, plano_repo, instituicao_repo, assinatura_repo
from data.model.assinatura_model import Assinatura

class TestAssinaturaRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = assinatura_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, cidade_exemplo, plano_exemplo, instituicao_exemplo, assinatura_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        plano_repo.criar_tabela()
        id_plano = plano_repo.inserir(plano_exemplo)

        instituicao_repo.criar_tabela()
        id_instituicao = instituicao_repo.inserir(instituicao_exemplo)

        assinatura_repo.criar_tabela()
        #Act
        id_tabela_inserida = assinatura_repo.inserir(assinatura_exemplo)
        #Assert
        dados_db = assinatura_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "A assinatura inserida não deveria ser None"
        assert dados_db.cod_assinatura == id_tabela_inserida, "O ID da assinatura inserida não confere"
        assert dados_db.cod_instituicao == id_instituicao, "O ID da instituição inserida não confere"
        assert dados_db.cod_plano == id_plano, "O ID do plano inserido não confere"
        assert dados_db.data_inicio.strftime("%Y-%m-%d") == "2025-01-01", "A data de início da assinatura inserida não confere"
        assert dados_db.data_fim.strftime("%Y-%m-%d") == "2025-01-01", "A data de fim da assinatura inserida não confere"
        assert dados_db.valor == float(10), "O valor da assinatura inserido não confere"
        assert dados_db.qtd_licenca == 10, "A quantidade da licença inserida não confere"


    def test_update_existente(self, test_db, instituicao_exemplo, cidade_exemplo, plano_exemplo, assinatura_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        plano_repo.criar_tabela()
        plano_repo.inserir(plano_exemplo)
        
        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)

        assinatura_repo.criar_tabela()
        id_tabela_inserida = assinatura_repo.inserir(assinatura_exemplo)
        
        tabela_inserida = assinatura_repo.obter_por_id(id_tabela_inserida)
            
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.data_inicio = "2000-01-01"
        tabela_inserida.data_fim = "2000-01-01"
        tabela_inserida.valor = float(20)
        tabela_inserida.qtd_licenca = 20
        resultado = assinatura_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = assinatura_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.data_inicio.strftime("%Y-%m-%d") == "2000-01-01", "A data início atualizada não confere"
        assert dados_db.data_fim.strftime("%Y-%m-%d") == "2000-01-01", "A data de fim não confere"
        assert dados_db.valor == float(20), "O valor atualizado não confere"
        assert dados_db.qtd_licenca == 20, "A quantidade licença atualizado não confere"

    def test_update_inexistente(self, test_db, assinatura_exemplo):
        #Arrange
        #Não é necessário inserir as tabelas anteriores        
        assinatura_repo.criar_tabela()
        assinatura_exemplo.cod_assinatura = 999  # ID inexistente
        #Act
        resultado = assinatura_repo.update(assinatura_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, instituicao_exemplo, cidade_exemplo, plano_exemplo, assinatura_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        plano_repo.criar_tabela()
        plano_repo.inserir(plano_exemplo)

        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)

        assinatura_repo.criar_tabela()
        id_tabela_inserida = assinatura_repo.inserir(assinatura_exemplo)                   
        #Act
        resultado = assinatura_repo.delete(id_tabela_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = assinatura_repo.obter_por_id(id_tabela_inserida)
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        plano_repo.criar_tabela()        
        instituicao_repo.criar_tabela()
        assinatura_repo.criar_tabela()
        #Act
        resultado = assinatura_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_instituicoes_exemplo, lista_cidades_exemplo, lista_planos_exemplo, lista_assinaturas_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        for cidade in lista_cidades_exemplo:
            cidade_repo.inserir(cidade)
        
        plano_repo.criar_tabela()
        for plano in lista_planos_exemplo:
            plano_repo.inserir(plano)
        
        instituicao_repo.criar_tabela()
        for instituicao in lista_instituicoes_exemplo:
            instituicao_repo.inserir(instituicao)
        
        assinatura_repo.criar_tabela()
        for assinatura in lista_assinaturas_exemplo:
            assinatura_repo.inserir(assinatura)
        #Act
        dados_db = assinatura_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(a, Assinatura) for a in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        cod_retornados = [a.cod_assinatura for a in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_instituicoes_exemplo, lista_planos_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        for cidade in lista_cidades_exemplo:
            cidade_repo.inserir(cidade)

        instituicao_repo.criar_tabela()
        for instituicao in lista_instituicoes_exemplo:
            instituicao_repo.inserir(instituicao)

        plano_repo.criar_tabela()
        for plano in lista_planos_exemplo:
            plano_repo.inserir(plano)

        assinatura_repo.criar_tabela()
        #Act
        dados_db = assinatura_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, instituicao_exemplo, plano_exemplo, assinatura_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        plano_repo.criar_tabela()
        id_plano = plano_repo.inserir(plano_exemplo)

        instituicao_repo.criar_tabela()
        id_instituicao = instituicao_repo.inserir(instituicao_exemplo)

        assinatura_repo.criar_tabela()
        id_tabela_inserida = assinatura_repo.inserir(assinatura_exemplo)
           
        #Act
        dados_db = assinatura_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "A Cidade obtida não deveria ser None"
        assert dados_db.cod_assinatura == id_tabela_inserida, "O ID da instituição obtida deveria ser igual ao ID da cidade inserido"
        assert dados_db.cod_instituicao == id_instituicao, "O cod_instituição obtido deveria ser igual ao id_instituição inserido"
        assert dados_db.cod_plano == id_plano, "O cod_plano obtido deveria ser igual ao id_plano inserido"
        assert dados_db.data_inicio.strftime("%Y-%m-%d") == "2025-01-01", "A data de início da assinatura obtida deveria ser igual a data de início da assinatura inserida"
        assert dados_db.data_fim.strftime("%Y-%m-%d") == "2025-01-01", "A data de fim da assinatura obtida deveria ser igual a data de fim da assinatura inserida"
        assert dados_db.valor == float(10), "O valor da assinatura obtida deveria ser igual ao valor da assinatura inserida"
        assert dados_db.qtd_licenca == 10, "A quantidade de licença da assinatura obtida deveria ser igual a quantidade de licença da assinatura inserida"

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, instituicao_exemplo, plano_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        plano_repo.criar_tabela()
        plano_repo.inserir(plano_exemplo)

        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)

        assinatura_repo.criar_tabela()
        #Act
        dados_db = assinatura_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"