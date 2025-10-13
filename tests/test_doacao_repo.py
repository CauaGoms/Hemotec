from data.repo import usuario_repo, doador_repo, cidade_repo, doacao_repo
from data.model.doacao_model import Doacao
from util.database import get_connection

class TestDoacaoRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = doacao_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, usuario_exemplo, doador_exemplo, cidade_exemplo, doacao_exemplo):
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
            conn.commit()

        doacao_repo.criar_tabela()
        doacao_exemplo.cod_doacao = id_usuario  
        # Act
        id_tabela_inserida = doacao_repo.inserir(doacao_exemplo)
        # Assert
        dados_db = doacao_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "A assinatura inserida não deveria ser None"
        assert dados_db.cod_doacao == id_usuario, "O ID do colaborador inserido não confere"
        assert dados_db.cod_doador == id_doador, "A função inserida não confere"
        assert dados_db.data_hora.strftime("%Y-%m-%d %H:%M:%S") == "2025-01-01 01:00:00", "A função inserida não confere"
        assert dados_db.quantidade == 10, "A função inserida não confere"
        assert dados_db.status == 1, "A função inserida não confere"
        
    def test_update_existente(self, test_db, usuario_exemplo, cidade_exemplo, doador_exemplo, doacao_exemplo):
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
            conn.commit()

        doacao_repo.criar_tabela()
        id_tabela_inserida = doacao_repo.inserir(doacao_exemplo)
        tabela_inserida = doacao_repo.obter_por_id(id_tabela_inserida)          
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.data_hora = "2025-01-01 00:00:00"
        tabela_inserida.quantidade = 10
        tabela_inserida.status = 1
        resultado = doacao_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = doacao_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.data_hora.strftime("%Y-%m-%d %H:%M:%S") == "2025-01-01 00:00:00", "A função atualizada não confere"
        assert dados_db.quantidade == 10, "A função atualizada não confere"
        assert dados_db.status == 1, "A função atualizada não confere"
       
    def test_update_inexistente(self, test_db, doacao_exemplo):
        #Arrange)
        cidade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        doador_repo.criar_tabela()
        doacao_repo.criar_tabela()
        doacao_exemplo.cod_doacao = 999  # ID inexistente
        #Act
        resultado = doacao_repo.update(doacao_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, usuario_exemplo, cidade_exemplo, doador_exemplo, doacao_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)

            doador_repo.criar_tabela(cursor)
            doador_exemplo.cod_doador = id_usuario
            id_doador = doador_repo.inserir(doador_exemplo, cursor)
            conn.commit()

        doacao_exemplo.cod_doacao = id_usuario
        doacao_repo.criar_tabela()
        id_tabela_inserida = doacao_repo.inserir(doacao_exemplo)                   
        #Act
        resultado = doacao_repo.delete(id_tabela_inserida)
            
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = doacao_repo.obter_por_id(id_tabela_inserida)     
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        usuario_repo.criar_tabela()        
        doador_repo.criar_tabela()
        doacao_repo.criar_tabela()
        #Act
        resultado = doacao_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_doadores_exemplo, lista_doacoes_exemplo):
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
            conn.commit()
        
        doacao_repo.criar_tabela()
        for doacao in lista_doacoes_exemplo:
            doacao_repo.inserir(doacao)
        #Act
        dados_db = doacao_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(c, Doacao) for c in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = []
        for doacao in dados_db:
            cod_esperados.append(doacao.cod_doacao)
        cod_retornados = [c.cod_doacao for c in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_doadores_exemplo, lista_doacoes_exemplo):
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
            conn.commit()

        doacao_repo.criar_tabela()
        #Act
        dados_db = doacao_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, usuario_exemplo, doador_exemplo, doacao_exemplo):
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
            conn.commit()

        doacao_exemplo.cod_doacao = id_usuario
        doacao_repo.criar_tabela()
        id_tabela_inserida = doacao_repo.inserir(doacao_exemplo)
           
        #Act
        dados_db = doacao_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "O Colaborador obtido não deveria ser None"
        assert dados_db.cod_doacao == id_tabela_inserida, "O ID do colaborador inserido não confere"
        assert dados_db.cod_doador == id_doador, "A função inserida não confere"
        assert dados_db.data_hora.strftime("%Y-%m-%d %H:%M:%S") == "2025-01-01 01:00:00", "A função inserida não confere"
        assert dados_db.quantidade == 10, "A função inserida não confere"
        assert dados_db.status == 1, "A função inserida não confere"

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, usuario_exemplo, doador_exemplo, doacao_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)

            doador_repo.criar_tabela(cursor)
            doador_exemplo.cod_doador = id_usuario
            doador_exemplo.cod_usuario = id_usuario
            id_doador = doador_repo.inserir(doador_exemplo, cursor)
            conn.commit()

        doacao_repo.criar_tabela()
        #Act
        dados_db = doacao_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"