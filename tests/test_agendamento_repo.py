from data.repo import usuario_repo, cidade_repo, agendamento_repo, doador_repo, colaborador_repo
from data.model.agendamento_model import Agendamento
from data.util.database import get_connection
from datetime import datetime

class TestAgendamentoRepo:
    def test_criar_tabela_agendamento(self, test_db):
        #Arrange
        #Act
        resultado = agendamento_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, usuario_exemplo, agendamento_exemplo, cidade_exemplo, doador_exemplo, colaborador_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_repo.criar_tabela()
        doador_exemplo.cod_doador = id_usuario
        id_doador = doador_repo.inserir(doador_exemplo)

        colaborador_repo.criar_tabela()
        colaborador_exemplo.cod_usuario = id_usuario
        id_colaborador = colaborador_repo.inserir(colaborador_exemplo)

        agendamento_repo.criar_tabela()
        agendamento_exemplo.cod_doador = id_doador
        agendamento_exemplo.cod_colaborador = id_colaborador

        #Act
        id_tabela_inserida = agendamento_repo.inserir(agendamento_exemplo)  
        #Assert
        dados_db = agendamento_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "A assinatura inserida não deveria ser None"
        assert dados_db.cod_agendamento == id_tabela_inserida, "O ID do colaborador inserido não confere"
        assert dados_db.cod_colaborador == id_colaborador, "O ID do colaborador inserido não confere"
        assert dados_db.cod_doador == id_doador, "O ID do colaborador inserido não confere"
        assert dados_db.data_hora.strftime('%Y-%m-%d %H:%M:%S') == "2025-01-01 01:00:00", "A data/hora não confere"
        assert dados_db.status == 1, "O ID do colaborador inserido não confere"
        assert dados_db.tipo_agendamento == "tipo_agendamento teste", "O ID do colaborador inserido não confere"

    def test_update_existente(self, test_db, usuario_exemplo, cidade_exemplo, colaborador_exemplo, doador_exemplo, agendamento_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_repo.criar_tabela()
        doador_exemplo.cod_doador = id_usuario
        id_doador = doador_repo.inserir(doador_exemplo)

        colaborador_repo.criar_tabela()
        colaborador_exemplo.cod_usuario = id_usuario
        id_colaborador = colaborador_repo.inserir(colaborador_exemplo)

        agendamento_repo.criar_tabela()
        agendamento_exemplo.cod_doador = id_doador
        agendamento_exemplo.cod_colaborador = id_colaborador

        #Act
        id_tabela_inserida = agendamento_repo.inserir(agendamento_exemplo)
        tabela_inserida = agendamento_repo.obter_por_id(id_tabela_inserida)           
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.data_hora = datetime(2025, 1, 2, 10, 0)
        tabela_inserida.status = "status atualizado"
        tabela_inserida.tipo_agendamento = "tipo_agendamento atualizada"
        resultado = agendamento_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = agendamento_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.data_hora == datetime(2025, 1, 2, 10, 0), "Data Hora"
        assert dados_db.status == "status atualizado"
        assert dados_db.tipo_agendamento == "tipo_agendamento atualizada"

    def test_update_inexistente(self, test_db, agendamento_exemplo):
        #Arrange)
        agendamento_repo.criar_tabela()
        agendamento_exemplo.cod_agendamento = 999  # ID inexistente
        #Act
        resultado = agendamento_repo.update(agendamento_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
    
    def test_delete_existente(self, test_db, usuario_exemplo, cidade_exemplo, doador_exemplo, gestor_exemplo, colaborador_exemplo, agendamento_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_repo.criar_tabela()
        doador_exemplo.cod_doador = id_usuario
        id_doador = doador_repo.inserir(doador_exemplo)

        colaborador_repo.criar_tabela()
        colaborador_exemplo.cod_usuario = id_usuario
        id_colaborador = colaborador_repo.inserir(colaborador_exemplo)

        agendamento_repo.criar_tabela()
        agendamento_exemplo.cod_doador = id_doador
        agendamento_exemplo.cod_colaborador = id_colaborador

        id_tabela_inserida = agendamento_repo.inserir(agendamento_exemplo)                   
        #Act
        resultado = agendamento_repo.delete(id_tabela_inserida)
            
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = agendamento_repo.obter_por_id(id_tabela_inserida)     
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"
    
    def test_delete_inexistente(self, test_db):
        #Arrange
        colaborador_repo.criar_tabela()
        doador_repo.criar_tabela()
        agendamento_repo.criar_tabela()
        #Act
        resultado = agendamento_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_doadores_exemplo, lista_colaboradores_exemplo, lista_agendamentos_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cidade_repo.criar_tabela()
            for cidade in lista_cidades_exemplo:
                cidade_repo.inserir(cidade)
        
            usuario_repo.criar_tabela()
            usuario_ids = []
            for usuario in lista_usuarios_exemplo:
                id_usuario = usuario_repo.inserir(usuario, cursor)
                usuario_ids.append(id_usuario)
            conn.commit()

        doador_repo.criar_tabela()
        doador_ids = []
        for i, doador in enumerate(lista_doadores_exemplo):
            doador.cod_usuario = usuario_ids[i]
            id_doador = doador_repo.inserir(doador)
            doador_ids.append(id_doador)

        colaborador_repo.criar_tabela()
        colaborador_ids = []
        for i, colaborador in enumerate(lista_colaboradores_exemplo):
            colaborador.cod_usuario = usuario_ids[i]
            id_colaborador = colaborador_repo.inserir(colaborador)
            colaborador_ids.append(id_colaborador)

        agendamento_repo.criar_tabela()
        for i, agendamento in enumerate(lista_agendamentos_exemplo):
            agendamento.cod_doador = doador_ids[i]
            agendamento.cod_colaborador = colaborador_ids[i]
            agendamento_repo.inserir(agendamento)
        #Act
        dados_db = agendamento_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(a, Agendamento) for a in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = []
        for agendamento in dados_db:
            cod_esperados.append(agendamento.cod_agendamento)
        cod_retornados = [a.cod_agendamento for a in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"
    
    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_doadores_exemplo, lista_colaboradores_exemplo):
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cidade_repo.criar_tabela()
            for cidade in lista_cidades_exemplo:
                cidade_repo.inserir(cidade)
        
            usuario_repo.criar_tabela()
            usuario_ids = []
            for usuario in lista_usuarios_exemplo:
                id_usuario = usuario_repo.inserir(usuario, cursor)
                usuario_ids.append(id_usuario)
            conn.commit()

        doador_repo.criar_tabela()
        doador_ids = []
        for i, doador in enumerate(lista_doadores_exemplo):
            doador.cod_usuario = usuario_ids[i]
            id_doador = doador_repo.inserir(doador)
            doador_ids.append(id_doador)

        colaborador_repo.criar_tabela()
        colaborador_ids = []
        for i, colaborador in enumerate(lista_colaboradores_exemplo):
            colaborador.cod_usuario = usuario_ids[i]
            id_colaborador = colaborador_repo.inserir(colaborador)
            colaborador_ids.append(id_colaborador)

        agendamento_repo.criar_tabela()
        #Act
        dados_db = agendamento_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"
    
    def test_obter_por_id_existente(self, test_db, cidade_exemplo, usuario_exemplo, doador_exemplo, gestor_exemplo, colaborador_exemplo, agendamento_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_repo.criar_tabela()
        doador_exemplo.cod_doador = id_usuario
        id_doador = doador_repo.inserir(doador_exemplo)

        colaborador_repo.criar_tabela()
        colaborador_exemplo.cod_usuario = id_usuario
        id_colaborador = colaborador_repo.inserir(colaborador_exemplo)

        agendamento_repo.criar_tabela()
        agendamento_exemplo.cod_doador = id_doador
        agendamento_exemplo.cod_colaborador = id_colaborador
        id_tabela_inserida = agendamento_repo.inserir(agendamento_exemplo)
           
        #Act
        dados_db = agendamento_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "O agendamento retornado não deveria ser None"
        assert dados_db.cod_agendamento == id_tabela_inserida, "O ID do agendamento não confere"
        assert dados_db.cod_colaborador == id_colaborador, "O ID do colaborador não confere"
        assert dados_db.cod_doador == id_doador, "O ID do doador não confere"
        assert dados_db.data_hora == datetime(2025, 1, 1, 1, 0), "A data e hora do agendamento não confere"
        assert dados_db.status == 1, "O status não confere"
        assert dados_db.tipo_agendamento == "tipo_agendamento teste", "O tipo de agendamento não confere"

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, usuario_exemplo, doador_exemplo, colaborador_exemplo):
        #Arrange        
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)
            
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_repo.criar_tabela()
        doador_exemplo.cod_usuario = id_usuario
        doador_exemplo.cod_doador = id_usuario  # Certifique-se de usar o mesmo ID
        doador_repo.inserir(doador_exemplo)

        colaborador_repo.criar_tabela()
        colaborador_exemplo.cod_usuario = id_usuario
        colaborador_exemplo.cod_colaborador = id_usuario
        colaborador_repo.inserir(colaborador_exemplo)

        agendamento_repo.criar_tabela()
        #Act
        dados_db = agendamento_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"