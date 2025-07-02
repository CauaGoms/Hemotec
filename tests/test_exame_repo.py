from data.repo import usuario_repo, doador_repo, cidade_repo, doacao_repo, exame_repo
from data.model.exame_model import Exame
from data.util.database import get_connection

class TestExameRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = exame_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, usuario_exemplo, doador_exemplo, cidade_exemplo, doacao_exemplo, exame_exemplo):
        # Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            doador_repo.criar_tabela(cursor)  
            doador_exemplo.cod_doador = id_usuario
            id_doador = doador_repo.inserir(doador_exemplo, cursor)
            doacao_repo.criar_tabela(cursor)
            id_doacao = doacao_repo.inserir(doacao_exemplo, cursor)
            conn.commit()

        exame_repo.criar_tabela()
        exame_exemplo.cod_exame = id_usuario  
        # Act
        id_tabela_inserida = exame_repo.inserir(exame_exemplo)
        # Assert
        dados_db = exame_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "A assinatura inserida não deveria ser None"
        assert dados_db.cod_exame == id_usuario, "O ID do colaborador inserido não confere"
        assert dados_db.cod_doacao == id_doacao, "A função inserida não confere"
        assert dados_db.data_exame.strftime("%Y-%m-%d %H:%M:%S") == "2025-01-01 00:00:00", "A função inserida não confere"
        assert dados_db.tipo_exame == "tipo_exame teste", "A função inserida não confere"
        assert dados_db.resultado == "resultado teste", "A função inserida não confere"
        assert dados_db.arquivo == "arquivo teste", "A função inserida não confere"
        
    def test_update_existente(self, test_db, usuario_exemplo, cidade_exemplo, doador_exemplo, doacao_exemplo, exame_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            doador_repo.criar_tabela(cursor)  
            doador_exemplo.cod_doador = id_usuario
            id_doador = doador_repo.inserir(doador_exemplo, cursor)
            doacao_repo.criar_tabela(cursor)
            id_doacao = doacao_repo.inserir(doacao_exemplo, cursor)
            conn.commit()

        exame_repo.criar_tabela()
        id_tabela_inserida = exame_repo.inserir(exame_exemplo)
        tabela_inserida = exame_repo.obter_por_id(id_tabela_inserida)          
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.data_exame = "2025-01-01 00:00:00"
        tabela_inserida.tipo_exame = "tipo_exame atualizado"
        tabela_inserida.resultado =  "resultado atualizado"
        tabela_inserida.arquivo = "arquivo atualizado"
        resultado = exame_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = exame_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.data_exame.strftime("%Y-%m-%d %H:%M:%S") == "2025-01-01 00:00:00", "A função atualizada não confere"
        assert dados_db.tipo_exame == "tipo_exame atualizado", "A função atualizada não confere"
        assert dados_db.resultado == "resultado atualizado", "A função atualizada não confere"
        assert dados_db.arquivo == "arquivo atualizado", "A função atualizada não confere"
       
    def test_update_inexistente(self, test_db, exame_exemplo):
        #Arrange)
        cidade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        doador_repo.criar_tabela()
        doacao_repo.criar_tabela()
        exame_repo.criar_tabela()
        exame_exemplo.cod_exame = 999  # ID inexistente
        #Act
        resultado = exame_repo.update(exame_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, usuario_exemplo, cidade_exemplo, doador_exemplo, doacao_exemplo, exame_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            doador_repo.criar_tabela(cursor)  
            doador_exemplo.cod_doador = id_usuario
            id_doador = doador_repo.inserir(doador_exemplo, cursor)
            doacao_repo.criar_tabela(cursor)
            id_doacao = doacao_repo.inserir(doacao_exemplo, cursor)
            conn.commit()

        exame_exemplo.cod_exame = id_usuario
        exame_repo.criar_tabela()
        id_tabela_inserida = exame_repo.inserir(exame_exemplo)                   
        #Act
        resultado = exame_repo.delete(id_tabela_inserida)
            
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = exame_repo.obter_por_id(id_tabela_inserida)     
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        usuario_repo.criar_tabela()        
        doador_repo.criar_tabela()
        doacao_repo.criar_tabela()
        exame_repo.criar_tabela()
        #Act
        resultado = exame_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_doadores_exemplo, lista_doacoes_exemplo, lista_exames_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            for cidade in lista_cidades_exemplo:
                cidade_repo.inserir(cidade)
        
            usuario_repo.criar_tabela()
            for usuario in lista_usuarios_exemplo:
                usuario_repo.inserir(usuario, cursor)

            doador_repo.criar_tabela(cursor)
            for doador in lista_doadores_exemplo:
                doador_repo.inserir(doador, cursor)

            doacao_repo.criar_tabela(cursor)
            for doacao in lista_doacoes_exemplo:
                doacao_repo.inserir(doacao, cursor)
            conn.commit()
        
        exame_repo.criar_tabela()
        for exame in lista_exames_exemplo:
            exame_repo.inserir(exame)
        #Act
        dados_db = exame_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(c, Exame) for c in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = []
        for exame in dados_db:
            cod_esperados.append(exame.cod_exame)
        cod_retornados = [c.cod_exame for c in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_doadores_exemplo, lista_doacoes_exemplo, lista_exames_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            for cidade in lista_cidades_exemplo:
                cidade_repo.inserir(cidade)
        
            usuario_repo.criar_tabela()
            for usuario in lista_usuarios_exemplo:
                usuario_repo.inserir(usuario, cursor)

            doador_repo.criar_tabela(cursor)
            for doador in lista_doadores_exemplo:
                doador_repo.inserir(doador, cursor)

            doacao_repo.criar_tabela(cursor)
            for doacao in lista_doacoes_exemplo:
                doacao_repo.inserir(doacao, cursor)
            conn.commit()

        exame_repo.criar_tabela()
        #Act
        dados_db = exame_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, usuario_exemplo, doador_exemplo, doacao_exemplo, exame_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)

            doador_repo.criar_tabela(cursor)
            doador_exemplo.cod_doador = id_usuario
            id_doador = doador_repo.inserir(doador_exemplo, cursor)

            doacao_repo.criar_tabela(cursor)
            id_doacao = doacao_repo.inserir(doacao_exemplo, cursor)
            conn.commit()

        exame_exemplo.cod_exame = id_usuario
        exame_repo.criar_tabela()
        id_tabela_inserida = exame_repo.inserir(exame_exemplo)
           
        #Act
        dados_db = exame_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "O Colaborador obtido não deveria ser None"
        assert dados_db.cod_exame == id_usuario, "O ID do colaborador inserido não confere"
        assert dados_db.cod_doacao == id_doacao, "A função inserida não confere"
        assert dados_db.data_exame.strftime("%Y-%m-%d %H:%M:%S") == "2025-01-01 00:00:00", "A função inserida não confere"
        assert dados_db.tipo_exame == "tipo_exame teste", "A função inserida não confere"
        assert dados_db.resultado == "resultado teste", "A função inserida não confere"
        assert dados_db.arquivo == "arquivo teste", "A função inserida não confere"

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, usuario_exemplo, doador_exemplo, doacao_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)

            doador_repo.criar_tabela(cursor)
            doador_exemplo.cod_doador = id_usuario
            id_doador = doador_repo.inserir(doador_exemplo, cursor)

            doacao_repo.criar_tabela(cursor)
            id_doacao = doacao_repo.inserir(doacao_exemplo, cursor)
            conn.commit()

        exame_repo.criar_tabela()
        #Act
        dados_db = exame_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"