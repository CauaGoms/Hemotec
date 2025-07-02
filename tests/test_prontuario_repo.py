from data.repo import prontuario_repo, usuario_repo, doador_repo, cidade_repo
from data.model.prontuario_model import Prontuario
from datetime import date
from data.util.database import get_connection

class TestProntuarioRepo:
    def test_criar_tabela_prontuario(self, test_db):
        #Arrange
        #Act
        resultado = prontuario_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, prontuario_exemplo, usuario_exemplo, doador_exemplo, cidade_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_repo.criar_tabela()
        doador_exemplo.cod_usuario = id_usuario
        doador_exemplo.cod_doador = id_usuario
        id_doador = doador_repo.inserir(doador_exemplo)

        prontuario_repo.criar_tabela()
        prontuario_exemplo.cod_doador = id_doador
        prontuario_exemplo.cod_prontuario = id_usuario
        #Act
        id_tabela_inserida = prontuario_repo.inserir(prontuario_exemplo)
        #Assert
        dados_db = prontuario_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "O prontuário retornado não deveria ser None"
        assert dados_db.cod_prontuario == id_tabela_inserida, "O ID do prontuário retornado está incorreto"
        assert dados_db.cod_doador == prontuario_exemplo.cod_doador, "O ID do doador associado está incorreto"
        assert dados_db.data_criacao.date() == prontuario_exemplo.data_criacao, "A data de criação está incorreta"
        assert dados_db.data_atualizacao.date() == prontuario_exemplo.data_atualizacao, "A data de atualização está incorreta"
        assert dados_db.diabetes == prontuario_exemplo.diabetes, "O campo 'diabetes' está incorreto"
        assert dados_db.hipertensao == prontuario_exemplo.hipertensao, "O campo 'hipertensão' está incorreto"
        assert dados_db.cardiopatia == prontuario_exemplo.cardiopatia, "O campo 'cardiopatia' está incorreto"
        assert dados_db.cancer == prontuario_exemplo.cancer, "O campo 'câncer' está incorreto"
        assert dados_db.nenhuma == prontuario_exemplo.nenhuma, "O campo 'nenhuma' está incorreto"
        assert dados_db.outros == prontuario_exemplo.outros, "O campo 'outros' está incorreto"
        assert dados_db.medicamentos == prontuario_exemplo.medicamentos, "O campo 'medicamentos' está incorreto"
        assert dados_db.fumante == prontuario_exemplo.fumante, "O campo 'fumante' está incorreto"
        assert dados_db.alcool == prontuario_exemplo.alcool, "O campo 'álcool' está incorreto"
        assert dados_db.atividade == prontuario_exemplo.atividade, "O campo 'atividade' está incorreto"
        assert dados_db.jejum == prontuario_exemplo.jejum, "O campo 'jejum' está incorreto"
        assert dados_db.sono == prontuario_exemplo.sono, "O campo 'sono' está incorreto"
        assert dados_db.bebida == prontuario_exemplo.bebida, "O campo 'bebida' está incorreto"
        assert dados_db.sintomas_gripais == prontuario_exemplo.sintomas_gripais, "O campo 'sintomas gripais' está incorreto"
        assert dados_db.tatuagem == prontuario_exemplo.tatuagem, "O campo 'tatuagem' está incorreto"
        assert dados_db.termos == prontuario_exemplo.termos, "O campo 'termos' está incorreto"
        assert dados_db.alerta == prontuario_exemplo.alerta, "O campo 'alerta' está incorreto"
    
    def test_update_existente(self, test_db, usuario_exemplo, cidade_exemplo, doador_exemplo, prontuario_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_repo.criar_tabela()
        doador_exemplo.cod_usuario = id_usuario
        doador_exemplo.cod_doador = id_usuario
        id_doador = doador_repo.inserir(doador_exemplo)

        prontuario_repo.criar_tabela()
        prontuario_exemplo.cod_doador = id_doador
        prontuario_exemplo.cod_prontuario = id_usuario
        id_tabela_inserida = prontuario_repo.inserir(prontuario_exemplo)
        tabela_inserida = prontuario_repo.obter_por_id(id_tabela_inserida)
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.data_criacao = date(2025, 1, 1)
        tabela_inserida.data_atualizacao = date(2025, 1, 1)
        tabela_inserida.diabetes = "diabetes atualizado"
        tabela_inserida.hipertensao = "hipertensao atualizado"
        tabela_inserida.cardiopatia = "cardiopatia atualizado"
        tabela_inserida.cancer = "cancer atualizado"
        tabela_inserida.nenhuma = "nenhuma atualizado"
        tabela_inserida.outros = "outros atualizado"
        tabela_inserida.medicamentos = "medicamentos atualizado"
        tabela_inserida.fumante = "fumante atualizado"
        tabela_inserida.alcool = "alcool atualizado"
        tabela_inserida.atividade = "atividade atualizado"
        tabela_inserida.jejum = "jejum atualizado"
        tabela_inserida.sono = "sono atualizado"
        tabela_inserida.bebida = "bebida atualizado"
        tabela_inserida.sintomas_gripais = "sintomas_gripais atualizado"
        tabela_inserida.tatuagem = "tatuagem atualizado"
        tabela_inserida.termos = "termos atualizado"
        tabela_inserida.alerta = "alerta atualizado"
        resultado = prontuario_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = prontuario_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.data_criacao.date() == date(2025, 1, 1), "A data de criação atualizada não confere"
        assert dados_db.data_atualizacao.date() == date(2025, 1, 1), "A data de atualização atualizada não confere"
        assert dados_db.diabetes == "diabetes atualizado", "Campo 'diabetes' atualizado não confere"
        assert dados_db.hipertensao == "hipertensao atualizado", "Campo 'hipertensao' atualizado não confere"
        assert dados_db.cardiopatia == "cardiopatia atualizado", "Campo 'cardiopatia' atualizado não confere"
        assert dados_db.cancer == "cancer atualizado", "Campo 'cancer' atualizado não confere"
        assert dados_db.nenhuma == "nenhuma atualizado", "Campo 'nenhuma' atualizado não confere"
        assert dados_db.outros == "outros atualizado", "Campo 'outros' atualizado não confere"
        assert dados_db.medicamentos == "medicamentos atualizado", "Campo 'medicamentos' atualizado não confere"
        assert dados_db.fumante == "fumante atualizado", "Campo 'fumante' atualizado não confere"
        assert dados_db.alcool == "alcool atualizado", "Campo 'alcool' atualizado não confere"
        assert dados_db.atividade == "atividade atualizado", "Campo 'atividade' atualizado não confere"
        assert dados_db.jejum == "jejum atualizado", "Campo 'jejum' atualizado não confere"
        assert dados_db.sono == "sono atualizado", "Campo 'sono' atualizado não confere"
        assert dados_db.bebida == "bebida atualizado", "Campo 'bebida' atualizado não confere"
        assert dados_db.sintomas_gripais == "sintomas_gripais atualizado", "Campo 'sintomas_gripais' atualizado não confere"
        assert dados_db.tatuagem == "tatuagem atualizado", "Campo 'tatuagem' atualizado não confere"
        assert dados_db.termos == "termos atualizado", "Campo 'termos' atualizado não confere"
        assert dados_db.alerta == "alerta atualizado", "Campo 'alerta' atualizado não confere"
    
    def test_update_inexistente(self, test_db, prontuario_exemplo):
        #Arrange
        usuario_repo.criar_tabela()
        doador_repo.criar_tabela()
        prontuario_repo.criar_tabela()
        prontuario_exemplo.cod_prontuario = 999  # ID inexistente
        #Act
        resultado = prontuario_repo.update(prontuario_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
    
    def test_delete_existente(self, test_db, usuario_exemplo, cidade_exemplo, doador_exemplo, prontuario_exemplo):
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
        doador_exemplo.cod_doador = id_usuario
        id_doador = doador_repo.inserir(doador_exemplo)

        prontuario_repo.criar_tabela()
        prontuario_exemplo.cod_doador = id_doador
        prontuario_exemplo.cod_prontuario = id_usuario

        id_tabela_inserida = prontuario_repo.inserir(prontuario_exemplo)                   
        #Act
        resultado = prontuario_repo.delete(id_tabela_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = prontuario_repo.obter_por_id(id_tabela_inserida)     
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"
    
    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        doador_repo.criar_tabela()
        prontuario_repo.criar_tabela()
        #Act
        resultado = prontuario_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"
    
    def test_obter_todos(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_prontuarios_exemplo, lista_doadores_exemplo):
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
        
        prontuario_repo.criar_tabela()
        for i, prontuario in enumerate(lista_prontuarios_exemplo):
            prontuario.cod_doador = doador_ids[i]
            prontuario_repo.inserir(prontuario)

        #Act
        dados_db = prontuario_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(p, Prontuario) for p in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = []
        for prontuario in dados_db:
            cod_esperados.append(prontuario.cod_prontuario)
        cod_retornados = [p.cod_prontuario for p in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"  

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_doadores_exemplo, lista_prontuarios_exemplo):
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

        prontuario_repo.criar_tabela()
        dados_db = prontuario_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, usuario_exemplo, doador_exemplo, prontuario_exemplo):
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
        doador_exemplo.cod_doador = id_usuario
        id_doador = doador_repo.inserir(doador_exemplo)

        prontuario_repo.criar_tabela()
        prontuario_exemplo.cod_doador = id_doador
        prontuario_exemplo.cod_prontuario = id_usuario

        id_tabela_inserida = prontuario_repo.inserir(prontuario_exemplo) 
           
        #Act
        dados_db = prontuario_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "O prontuário retornado não deveria ser None"
        assert dados_db.cod_prontuario == id_tabela_inserida, "O ID do prontuário retornado está incorreto"
        assert dados_db.cod_doador == prontuario_exemplo.cod_doador, "O ID do doador associado está incorreto"

        # Conversão para comparar datetime e date
        assert dados_db.data_criacao.date() == prontuario_exemplo.data_criacao, "A data de criação não confere"
        assert dados_db.data_atualizacao.date() == prontuario_exemplo.data_atualizacao, "A data de atualização não confere"

        assert dados_db.diabetes == prontuario_exemplo.diabetes, "O campo 'diabetes' não confere"
        assert dados_db.hipertensao == prontuario_exemplo.hipertensao, "O campo 'hipertensao' não confere"
        assert dados_db.cardiopatia == prontuario_exemplo.cardiopatia, "O campo 'cardiopatia' não confere"
        assert dados_db.cancer == prontuario_exemplo.cancer, "O campo 'cancer' não confere"
        assert dados_db.nenhuma == prontuario_exemplo.nenhuma, "O campo 'nenhuma' não confere"
        assert dados_db.outros == prontuario_exemplo.outros, "O campo 'outros' não confere"
        assert dados_db.medicamentos == prontuario_exemplo.medicamentos, "O campo 'medicamentos' não confere"
        assert dados_db.fumante == prontuario_exemplo.fumante, "O campo 'fumante' não confere"
        assert dados_db.alcool == prontuario_exemplo.alcool, "O campo 'alcool' não confere"
        assert dados_db.atividade == prontuario_exemplo.atividade, "O campo 'atividade' não confere"
        assert dados_db.jejum == prontuario_exemplo.jejum, "O campo 'jejum' não confere"
        assert dados_db.sono == prontuario_exemplo.sono, "O campo 'sono' não confere"
        assert dados_db.bebida == prontuario_exemplo.bebida, "O campo 'bebida' não confere"
        assert dados_db.sintomas_gripais == prontuario_exemplo.sintomas_gripais, "O campo 'sintomas_gripais' não confere"
        assert dados_db.tatuagem == prontuario_exemplo.tatuagem, "O campo 'tatuagem' não confere"
        assert dados_db.termos == prontuario_exemplo.termos, "O campo 'termos' não confere"
        assert dados_db.alerta == prontuario_exemplo.alerta, "O campo 'alerta' não confere"

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, usuario_exemplo, prontuario_exemplo, doador_exemplo):
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
        doador_exemplo.cod_doador = id_usuario
        id_doador = doador_repo.inserir(doador_exemplo)

        prontuario_repo.criar_tabela()
        prontuario_exemplo.cod_doador = id_doador
        prontuario_exemplo.cod_prontuario = id_usuario
        #Act
        dados_db = prontuario_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"