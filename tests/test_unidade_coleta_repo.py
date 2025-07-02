from data.repo import cidade_repo, instituicao_repo, plano_repo, licenca_repo, assinatura_repo, unidade_coleta_repo
from data.model.unidade_coleta_model import Unidade_coleta

class TestUnidade_coletaRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = unidade_coleta_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, licenca_exemplo, assinatura_exemplo, cidade_exemplo, instituicao_exemplo, plano_exemplo, unidade_coleta_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        id_cidade = cidade_repo.inserir(cidade_exemplo)

        plano_repo.criar_tabela()
        plano_repo.inserir(plano_exemplo)

        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)

        assinatura_repo.criar_tabela()
        id_assinatura = assinatura_repo.inserir(assinatura_exemplo)

        licenca_repo.criar_tabela()
        id_licenca = licenca_repo.inserir(licenca_exemplo)

        unidade_coleta_repo.criar_tabela()
        id_coleta = unidade_coleta_exemplo.cod_unidade
        id_unidade = unidade_coleta_repo.inserir(unidade_coleta_exemplo)
        dados_db = unidade_coleta_repo.obter_por_id(id_unidade)
        assert dados_db is not None, "A licenca inserida não deveria ser None"
        assert dados_db.cod_unidade == 1, "O ID da unidade inserida não confere"
        assert dados_db.cod_licenca == id_licenca, "O ID da licenca inserida não confere"
        assert dados_db.nome == "nome teste", "O nome inserido não confere"
        assert dados_db.email == "email teste", "O email inserido não confere"
        assert dados_db.rua_unidade == "rua_unidade teste", "O rua_unidade inserido não confere"
        assert dados_db.bairro_unidade == "bairro_unidade teste", "O bairro_unidade inserido não confere"
        assert dados_db.cidade_unidade == id_cidade, "O nome inserido não confere"
        assert dados_db.cep_unidade == "cep_unidade teste", "O nome inserido não confere"
        assert dados_db.latitude == 10.0, "O nome inserido não confere"
        assert dados_db.longitude == 10.0, "O nome inserido não confere"
        assert dados_db.telefone == "telefone teste", "O nome inserido não confere"


    def test_update_existente(self, test_db, licenca_exemplo, assinatura_exemplo, cidade_exemplo, instituicao_exemplo, plano_exemplo, unidade_coleta_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        id_cidade =cidade_repo.inserir(cidade_exemplo)

        plano_repo.criar_tabela()
        plano_repo.inserir(plano_exemplo)

        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)

        assinatura_repo.criar_tabela()
        id_assinatura = assinatura_repo.inserir(assinatura_exemplo)

        licenca_repo.criar_tabela()
        id_licenca = licenca_repo.inserir(licenca_exemplo)

        unidade_coleta_repo.criar_tabela()
        # unidade_coleta_exemplo.cod_unidade = id_unidade
        id_tabela_inserida = unidade_coleta_repo.inserir(unidade_coleta_exemplo)
        tabela_inserida = unidade_coleta_repo.obter_por_id(id_tabela_inserida)
            
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.status = 1
        resultado = unidade_coleta_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = unidade_coleta_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.nome == "nome teste", "O status atualizado não confere"
        assert dados_db.email == "email teste", "O email inserido não confere"
        assert dados_db.rua_unidade == "rua_unidade teste", "O rua_unidade inserido não confere"
        assert dados_db.bairro_unidade == "bairro_unidade teste", "O bairro_unidade inserido não confere"
        assert dados_db.cidade_unidade == id_cidade, "O nome inserido não confere"
        assert dados_db.cep_unidade == "cep_unidade teste", "O nome inserido não confere"
        assert dados_db.latitude == 10.0, "O nome inserido não confere"
        assert dados_db.longitude == 10.0, "O nome inserido não confere"
        assert dados_db.telefone == "telefone teste", "O nome inserido não confere"

    def test_update_inexistente(self, test_db, unidade_coleta_exemplo):
        #Arrange
        #Não é necessário inserir as tabelas anteriores  
        cidade_repo.criar_tabela()
        plano_repo.criar_tabela()
        instituicao_repo.criar_tabela()
        assinatura_repo.criar_tabela()
        licenca_repo.criar_tabela()      
        unidade_coleta_repo.criar_tabela()
        unidade_coleta_exemplo.cod_unidade = 999  # ID inexistente
        #Act
        resultado = unidade_coleta_repo.update(unidade_coleta_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, licenca_exemplo, assinatura_exemplo, cidade_exemplo, instituicao_exemplo, plano_exemplo, unidade_coleta_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        plano_repo.criar_tabela()
        plano_repo.inserir(plano_exemplo)

        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)

        assinatura_repo.criar_tabela()
        id_assinatura = assinatura_repo.inserir(assinatura_exemplo)

        licenca_repo.criar_tabela()
        licenca_repo.inserir(licenca_exemplo)

        unidade_coleta_repo.criar_tabela()
        id_tabela_inserida = unidade_coleta_repo.inserir(unidade_coleta_exemplo)
                  
        #Act
        resultado = unidade_coleta_repo.delete(id_tabela_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = unidade_coleta_repo.obter_por_id(id_tabela_inserida)
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        plano_repo.criar_tabela()        
        instituicao_repo.criar_tabela()
        assinatura_repo.criar_tabela()
        licenca_repo.criar_tabela()
        unidade_coleta_repo.criar_tabela()
        #Act
        resultado = unidade_coleta_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_instituicoes_exemplo, lista_cidades_exemplo, lista_planos_exemplo, lista_assinaturas_exemplo, lista_licencas_exemplo, lista_unidades_coleta_exemplo):
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

        licenca_repo.criar_tabela()
        for licenca in lista_licencas_exemplo:
            licenca_repo.inserir(licenca)

        unidade_coleta_repo.criar_tabela()
        for unidade_coleta in lista_unidades_coleta_exemplo:
            unidade_coleta_repo.inserir(unidade_coleta)
        #Act
        dados_db = unidade_coleta_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(a, Unidade_coleta) for a in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        cod_retornados = [a.cod_unidade for a in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_instituicoes_exemplo, lista_planos_exemplo, lista_assinaturas_exemplo, lista_licencas_exemplo):
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
        for assinatura in lista_assinaturas_exemplo:
            assinatura_repo.inserir(assinatura)

        licenca_repo.criar_tabela()
        for licenca in lista_licencas_exemplo:
            licenca_repo.inserir(licenca)

        unidade_coleta_repo.criar_tabela()
        #Act
        dados_db = unidade_coleta_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, instituicao_exemplo, plano_exemplo, assinatura_exemplo, licenca_exemplo, unidade_coleta_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        id_cidade = cidade_repo.inserir(cidade_exemplo)

        plano_repo.criar_tabela()
        id_plano = plano_repo.inserir(plano_exemplo)

        instituicao_repo.criar_tabela()
        id_instituicao = instituicao_repo.inserir(instituicao_exemplo)

        assinatura_repo.criar_tabela()
        id_assinatura = assinatura_repo.inserir(assinatura_exemplo)

        licenca_repo.criar_tabela()
        id_licenca = licenca_repo.inserir(licenca_exemplo)

        unidade_coleta_repo.criar_tabela()
        id_tabela_inserida = unidade_coleta_repo.inserir(unidade_coleta_exemplo)

           
        #Act
        dados_db = unidade_coleta_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "A Cidade obtida não deveria ser None"
        assert dados_db.cod_unidade == id_tabela_inserida, "O ID da instituição obtida deveria ser igual ao ID da cidade inserido"
        assert dados_db.cod_licenca == id_licenca, "O cod_assinatura obtido deveria ser igual ao id_assinatura inserido"
        assert dados_db.nome == unidade_coleta_exemplo.nome, "O status obtido deveria ser igual ao status inserido"
        assert dados_db.email == unidade_coleta_exemplo.email, "O status obtido deveria ser igual ao status inserido"
        assert dados_db.rua_unidade == unidade_coleta_exemplo.rua_unidade, "O status obtido deveria ser igual ao status inserido"
        assert dados_db.bairro_unidade == unidade_coleta_exemplo.bairro_unidade, "O status obtido deveria ser igual ao status inserido"
        assert dados_db.cidade_unidade == id_cidade, "O status obtido deveria ser igual ao status inserido"
        assert dados_db.cep_unidade == unidade_coleta_exemplo.cep_unidade, "O status obtido deveria ser igual ao status inserido"
        assert dados_db.latitude == unidade_coleta_exemplo.latitude, "O status obtido deveria ser igual ao status inserido"
        assert dados_db.longitude == unidade_coleta_exemplo.longitude, "O status obtido deveria ser igual ao status inserido"
        assert dados_db.telefone == unidade_coleta_exemplo.telefone, "O status obtido deveria ser igual ao status inserido"

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, instituicao_exemplo, plano_exemplo, assinatura_exemplo, licenca_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        plano_repo.criar_tabela()
        plano_repo.inserir(plano_exemplo)

        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)

        assinatura_repo.criar_tabela()
        assinatura_repo.inserir(assinatura_exemplo)

        licenca_repo.criar_tabela()
        licenca_repo.inserir(licenca_exemplo)

        unidade_coleta_repo.criar_tabela()
        #Act
        dados_db = unidade_coleta_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"