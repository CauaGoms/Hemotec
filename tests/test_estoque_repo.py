from data.repo import cidade_repo, instituicao_repo, plano_repo, licenca_repo, assinatura_repo, unidade_coleta_repo, estoque_repo
from data.model.estoque_model import Estoque
from datetime import datetime

class TestEstoqueRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = estoque_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, licenca_exemplo, assinatura_exemplo, cidade_exemplo, instituicao_exemplo, plano_exemplo, unidade_coleta_exemplo, estoque_exemplo):
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
        id_unidade = unidade_coleta_repo.inserir(unidade_coleta_exemplo)

        estoque_repo.criar_tabela()
        id_coleta = estoque_exemplo.cod_estoque
        id_estoque = estoque_repo.inserir(estoque_exemplo)
        dados_db = estoque_repo.obter_por_id(id_estoque)
        assert dados_db is not None, "A licenca inserida não deveria ser None"
        assert dados_db.cod_estoque == 1, "O ID da unidade inserida não confere"
        assert dados_db.cod_unidade == id_unidade, "O ID da licenca inserida não confere"
        assert dados_db.tipo_sanguineo == "tipo_sanguineo teste", "O nome inserido não confere"
        assert dados_db.fator_rh == "fator_rh teste", "O email inserido não confere"
        assert dados_db.quantidade == 10, "O rua_unidade inserido não confere"
        assert dados_db.data_atualizacao.strftime('%Y-%m-%d') == "2025-01-01", "O bairro_unidade inserido não confere"


    def test_update_existente(self, test_db, licenca_exemplo, assinatura_exemplo, cidade_exemplo, instituicao_exemplo, plano_exemplo, unidade_coleta_exemplo, estoque_exemplo):
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
        id_unidade = unidade_coleta_repo.inserir(unidade_coleta_exemplo)

        estoque_repo.criar_tabela()
        id_tabela_inserida = estoque_repo.inserir(estoque_exemplo)
        tabela_inserida = estoque_repo.obter_por_id(id_tabela_inserida)
            
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.status = 1
        resultado = estoque_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = estoque_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.cod_estoque == 1, "O ID da unidade inserida não confere"
        assert dados_db.cod_unidade == id_unidade, "O ID da licenca inserida não confere"
        assert dados_db.tipo_sanguineo == "tipo_sanguineo teste", "O nome inserido não confere"
        assert dados_db.fator_rh == "fator_rh teste", "O email inserido não confere"
        assert dados_db.quantidade == 10, "O rua_unidade inserido não confere"
        assert dados_db.data_atualizacao.strftime('%Y-%m-%d %H:%M:%S') == "2025-01-01 00:00:00", "O bairro_unidade inserido não confere"

    def test_update_inexistente(self, test_db, estoque_exemplo):
        #Arrange
        #Não é necessário inserir as tabelas anteriores  
        cidade_repo.criar_tabela()
        plano_repo.criar_tabela()
        instituicao_repo.criar_tabela()
        assinatura_repo.criar_tabela()
        licenca_repo.criar_tabela()      
        unidade_coleta_repo.criar_tabela()
        estoque_repo.criar_tabela()
        estoque_exemplo.cod_estoque = 999  # ID inexistente
        #Act
        resultado = estoque_repo.update(estoque_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, licenca_exemplo, assinatura_exemplo, cidade_exemplo, instituicao_exemplo, plano_exemplo, unidade_coleta_exemplo, estoque_exemplo):
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
        id_unidade = unidade_coleta_repo.inserir(unidade_coleta_exemplo)

        estoque_repo.criar_tabela()
        id_tabela_inserida = estoque_repo.inserir(estoque_exemplo)
                  
        #Act
        resultado = estoque_repo.delete(id_tabela_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = estoque_repo.obter_por_id(id_tabela_inserida)
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        plano_repo.criar_tabela()        
        instituicao_repo.criar_tabela()
        assinatura_repo.criar_tabela()
        licenca_repo.criar_tabela()
        unidade_coleta_repo.criar_tabela()
        estoque_repo.criar_tabela()
        #Act
        resultado = estoque_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_instituicoes_exemplo, lista_cidades_exemplo, lista_planos_exemplo, lista_assinaturas_exemplo, lista_licencas_exemplo, lista_unidades_coleta_exemplo, lista_estoques_exemplo):
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

        estoque_repo.criar_tabela()
        for estoque in lista_estoques_exemplo:
            estoque_repo.inserir(estoque)
        #Act
        dados_db = estoque_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(a, Estoque) for a in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        cod_retornados = [a.cod_estoque for a in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_instituicoes_exemplo, lista_planos_exemplo, lista_assinaturas_exemplo, lista_licencas_exemplo, lista_unidades_coleta_exemplo):
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
        for unidade_coleta in lista_unidades_coleta_exemplo:
            unidade_coleta_repo.inserir(unidade_coleta)

        estoque_repo.criar_tabela()
        #Act
        dados_db = estoque_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, instituicao_exemplo, plano_exemplo, assinatura_exemplo, licenca_exemplo, unidade_coleta_exemplo, estoque_exemplo):
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
        id_unidade = unidade_coleta_repo.inserir(unidade_coleta_exemplo)

        estoque_repo.criar_tabela()
        id_tabela_inserida = estoque_repo.inserir(estoque_exemplo)

           
        #Act
        dados_db = estoque_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "A Cidade obtida não deveria ser None"
        assert dados_db.cod_estoque == 1, "O ID da unidade inserida não confere"
        assert dados_db.cod_unidade == id_unidade, "O ID da licenca inserida não confere"
        assert dados_db.tipo_sanguineo == "tipo_sanguineo teste", "O nome inserido não confere"
        assert dados_db.fator_rh == "fator_rh teste", "O email inserido não confere"
        assert dados_db.quantidade == 10, "O rua_unidade inserido não confere"
        assert dados_db.data_atualizacao.strftime('%Y-%m-%d %H:%M:%S') == "2025-01-01 00:00:00", "O bairro_unidade inserido não confere"

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, instituicao_exemplo, plano_exemplo, assinatura_exemplo, licenca_exemplo, unidade_coleta_exemplo):
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
        unidade_coleta_repo.inserir(unidade_coleta_exemplo)

        estoque_repo.criar_tabela()
        #Act
        dados_db = estoque_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"