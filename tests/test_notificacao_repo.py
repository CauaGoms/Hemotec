from data.repo import cidade_repo, instituicao_repo, plano_repo, licenca_repo, assinatura_repo, unidade_coleta_repo, adm_unidade_repo, usuario_repo, notificacao_repo
from data.model.notificacao_model import Notificacao
from data.util.database import get_connection

class TestNotificacaoRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = notificacao_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, licenca_exemplo, assinatura_exemplo, cidade_exemplo, instituicao_exemplo, plano_exemplo, unidade_coleta_exemplo, adm_unidade_exemplo, usuario_exemplo, notificacao_exemplo):
        cidade_repo.criar_tabela()
        plano_repo.criar_tabela()
        instituicao_repo.criar_tabela()
        assinatura_repo.criar_tabela()
        licenca_repo.criar_tabela()
        unidade_coleta_repo.criar_tabela()
        usuario_repo.criar_tabela()
        adm_unidade_repo.criar_tabela()
        notificacao_repo.criar_tabela()
        #Act
        with get_connection() as conn:
            cursor = conn.cursor()
            
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            plano_repo.inserir(plano_exemplo)
            instituicao_repo.inserir(instituicao_exemplo)
            id_assinatura = assinatura_repo.inserir(assinatura_exemplo)
            id_licenca = licenca_repo.inserir(licenca_exemplo)
            id_unidade = unidade_coleta_repo.inserir(unidade_coleta_exemplo)
            id_usuario = adm_unidade_exemplo.cod_adm
            id_adm = adm_unidade_repo.inserir(adm_unidade_exemplo, cursor)
            id_notificacao = notificacao_repo.inserir(notificacao_exemplo, cursor)
            conn.commit()  
            dados_db = notificacao_repo.obter_por_id(id_notificacao)
            assert dados_db is not None, "A licenca inserida não deveria ser None"
            assert dados_db.cod_notificacao == id_notificacao, "O ID da unidade inserida não confere"
            assert dados_db.cod_adm == id_adm, "O nome inserido não confere"
            assert dados_db.tipo == "tipo teste", "O ID da unidade inserida não confere"
            assert dados_db.mensagem == "mensagem teste", "O ID da unidade inserida não confere"
            assert dados_db.status == 1, "O status inserido não confere"
            assert dados_db.data_envio.strftime('%Y-%m-%d') == "2025-01-01", "O ID da unidade inserida não confere"



    def test_update_existente(self, test_db, licenca_exemplo, assinatura_exemplo, cidade_exemplo, instituicao_exemplo, plano_exemplo, unidade_coleta_exemplo, adm_unidade_exemplo, notificacao_exemplo):
        cidade_repo.criar_tabela()
        plano_repo.criar_tabela()
        instituicao_repo.criar_tabela()
        assinatura_repo.criar_tabela()
        licenca_repo.criar_tabela()
        unidade_coleta_repo.criar_tabela()
        usuario_repo.criar_tabela()
        adm_unidade_repo.criar_tabela()
        notificacao_repo.criar_tabela()
        #Act
        with get_connection() as conn:
            cursor = conn.cursor()
            
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            plano_repo.inserir(plano_exemplo)
            instituicao_repo.inserir(instituicao_exemplo)
            id_assinatura = assinatura_repo.inserir(assinatura_exemplo)
            id_licenca = licenca_repo.inserir(licenca_exemplo)
            id_unidade = unidade_coleta_repo.inserir(unidade_coleta_exemplo)
            id_usuario = adm_unidade_exemplo.cod_adm
            id_adm = adm_unidade_repo.inserir(adm_unidade_exemplo, cursor)
            id_notificacao = notificacao_repo.inserir(notificacao_exemplo, cursor)
            conn.commit()   

        tabela_inserida = notificacao_repo.obter_por_id(id_notificacao)
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.status = 1
        resultado = notificacao_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = notificacao_repo.obter_por_id(id_adm)
        assert dados_db is not None, "A licenca inserida não deveria ser None"
        assert dados_db is not None, "A licenca inserida não deveria ser None"
        assert dados_db.cod_notificacao == id_notificacao, "O ID da unidade inserida não confere"
        assert dados_db.cod_adm == id_adm, "O nome inserido não confere"
        assert dados_db.tipo == "tipo teste", "O ID da unidade inserida não confere"
        assert dados_db.mensagem == "mensagem teste", "O ID da unidade inserida não confere"
        assert dados_db.status == 1, "O status inserido não confere"
        assert dados_db.data_envio.strftime('%Y-%m-%d') == "2025-01-01", "O ID da unidade inserida não confere"

    def test_update_inexistente(self, test_db, notificacao_exemplo):
        #Arrange
        #Não é necessário inserir as tabelas anteriores  
        cidade_repo.criar_tabela()
        plano_repo.criar_tabela()
        instituicao_repo.criar_tabela()
        assinatura_repo.criar_tabela()
        licenca_repo.criar_tabela()      
        unidade_coleta_repo.criar_tabela()
        usuario_repo.criar_tabela()
        adm_unidade_repo.criar_tabela()
        notificacao_repo.criar_tabela()
        notificacao_exemplo.cod_adm = 999  # ID inexistente
        #Act
        resultado = notificacao_repo.update(notificacao_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, licenca_exemplo, assinatura_exemplo, cidade_exemplo, instituicao_exemplo, plano_exemplo, unidade_coleta_exemplo, adm_unidade_exemplo, usuario_exemplo, notificacao_exemplo):
        cidade_repo.criar_tabela()
        plano_repo.criar_tabela()
        instituicao_repo.criar_tabela()
        assinatura_repo.criar_tabela()
        licenca_repo.criar_tabela()
        unidade_coleta_repo.criar_tabela()
        usuario_repo.criar_tabela()
        adm_unidade_repo.criar_tabela()
        notificacao_repo.criar_tabela()
        #Act
        with get_connection() as conn:
            cursor = conn.cursor()
            
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            plano_repo.inserir(plano_exemplo)
            instituicao_repo.inserir(instituicao_exemplo)
            id_assinatura = assinatura_repo.inserir(assinatura_exemplo)
            id_licenca = licenca_repo.inserir(licenca_exemplo)
            id_unidade = unidade_coleta_repo.inserir(unidade_coleta_exemplo)
            id_usuario = adm_unidade_exemplo.cod_adm
            id_adm = adm_unidade_repo.inserir(adm_unidade_exemplo, cursor)
            id_notificacao = notificacao_repo.inserir(notificacao_exemplo, cursor)
            conn.commit() 

        notificacao_repo.criar_tabela()
        id_tabela_inserida = notificacao_repo.inserir(notificacao_exemplo)
                  
        #Act
        resultado = notificacao_repo.delete(id_tabela_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = notificacao_repo.obter_por_id(id_tabela_inserida)
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        plano_repo.criar_tabela()        
        instituicao_repo.criar_tabela()
        assinatura_repo.criar_tabela()
        licenca_repo.criar_tabela()
        unidade_coleta_repo.criar_tabela()
        usuario_repo.criar_tabela()
        adm_unidade_repo.criar_tabela()
        notificacao_repo.criar_tabela()
        #Act
        resultado = notificacao_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_instituicoes_exemplo, lista_cidades_exemplo, lista_planos_exemplo, lista_assinaturas_exemplo, lista_licencas_exemplo, lista_unidades_coleta_exemplo, lista_usuarios_exemplo, lista_adm_unidades_exemplo, lista_notificacoes_exemplo):
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

        usuario_repo.criar_tabela()

        adm_unidade_repo.criar_tabela()
        for adm_unidade in lista_adm_unidades_exemplo:
            adm_unidade_repo.inserir(adm_unidade)

        notificacao_repo.criar_tabela()
        for notificacao in lista_notificacoes_exemplo:
            notificacao_repo.inserir(notificacao)

        #Act
        dados_db = notificacao_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(a, Notificacao) for a in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        cod_retornados = [a.cod_notificacao for a in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_instituicoes_exemplo, lista_planos_exemplo, lista_assinaturas_exemplo, lista_licencas_exemplo, lista_adm_unidades_exemplo, lista_usuarios_exemplo, lista_unidades_coleta_exemplo, lista_notificacoes_exemplo):
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

        usuario_repo.criar_tabela()

        adm_unidade_repo.criar_tabela()
        for adm_unidade in lista_adm_unidades_exemplo:
            adm_unidade_repo.inserir(adm_unidade)

        notificacao_repo.criar_tabela()

        #Act
        dados_db = notificacao_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, instituicao_exemplo, plano_exemplo, assinatura_exemplo, licenca_exemplo, unidade_coleta_exemplo, adm_unidade_exemplo, usuario_exemplo, notificacao_exemplo):
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

        usuario_repo.criar_tabela()

        adm_unidade_repo.criar_tabela()
        id_adm_unidade = adm_unidade_repo.inserir(adm_unidade_exemplo)

        notificacao_repo.criar_tabela()
        id_tabela_inserida = notificacao_repo.inserir(notificacao_exemplo)

           
        #Act
        dados_db = notificacao_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db.cod_notificacao == id_tabela_inserida, "O ID da unidade inserida não confere"
        assert dados_db.cod_adm == id_adm_unidade, "O nome inserido não confere"
        assert dados_db.tipo == "tipo teste", "O ID da unidade inserida não confere"
        assert dados_db.mensagem == "mensagem teste", "O ID da unidade inserida não confere"
        assert dados_db.status == 1, "O status inserido não confere"
        assert dados_db.data_envio.strftime('%Y-%m-%d') == "2025-01-01", "O ID da unidade inserida não confere"
        
    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, instituicao_exemplo, plano_exemplo, assinatura_exemplo, licenca_exemplo, unidade_coleta_exemplo, adm_unidade_exemplo, usuario_exemplo, notificacao_exemplo):
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

        usuario_repo.criar_tabela()

        adm_unidade_repo.criar_tabela()
        adm_unidade_repo.inserir(adm_unidade_exemplo)

        notificacao_repo.criar_tabela()
        #Act
        dados_db = notificacao_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"