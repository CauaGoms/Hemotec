from data.repo import usuario_repo, colaborador_repo, cidade_repo
from data.model.colaborador_model import Colaborador
from data.util.database import get_connection

class TestColaboradorRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = colaborador_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, usuario_exemplo, colaborador_exemplo, cidade_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        colaborador_repo.criar_tabela()
        colaborador_exemplo.cod_colaborador = id_usuario  
        # colaborador_exemplo.cod_usuario = id_usuario      
        #Act
        id_tabela_inserida = colaborador_repo.inserir(colaborador_exemplo)
        #Assert
        dados_db = colaborador_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "A assinatura inserida não deveria ser None"
        assert dados_db.cod_colaborador == id_tabela_inserida, "O ID do colaborador inserido não confere"
        assert dados_db.funcao == "funcao teste", "A função inserida não confere"
        assert dados_db.cod_usuario == id_tabela_inserida, "O ID do plano inserido não confere"
        assert dados_db.nome == "nome teste", "O nome inserido não confere"
        assert dados_db.email == "email teste", "O email inserido não confere"
        assert dados_db.senha == "senha teste", "A senha inserida não confere"
        assert dados_db.cpf == "cpf teste", "O cpf inserido não confere"
        assert dados_db.data_nascimento.strftime("%Y-%m-%d") == "2025-01-01", "A data de nascimento inserida não confere"
        assert dados_db.status == True, "O status inserido não confere"
        assert dados_db.data_cadastro.strftime("%Y-%m-%d") == "2025-01-01", "A data de cadastro inserida não confere"
        assert dados_db.rua_usuario == "rua_usuario teste", "A rua_usuário inserida não confere"
        assert dados_db.bairro_usuario == "bairro_usuario teste", "O bairro do usuário inserido não confere"
        assert dados_db.cidade_usuario == id_cidade, "A cidade do usuário inserido não confere"
        assert dados_db.cep_usuario == "cep_usuario teste", "O cep do usuário inserido não confere"
        assert dados_db.telefone == "telefone teste", "O telefone inserido não confere"


    def test_update_existente(self, test_db, usuario_exemplo, cidade_exemplo, colaborador_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        colaborador_repo.criar_tabela()
        id_tabela_inserida = colaborador_repo.inserir(colaborador_exemplo)
        tabela_inserida = colaborador_repo.obter_por_id(id_tabela_inserida)          
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.funcao = "funcao atualizada"
        tabela_inserida.nome = "nome atualizado"
        tabela_inserida.email = "email atualizado"
        tabela_inserida.senha = "senha atualizada"
        tabela_inserida.cpf = "cpf atualizado"
        tabela_inserida.data_nascimento = "2000-01-01"
        tabela_inserida.status = False
        tabela_inserida.data_cadastro = "2000-01-01"
        tabela_inserida.rua_usuario = "rua_usuario atualizada"
        tabela_inserida.bairro_usuario = "bairro_usuario atualizado"
        tabela_inserida.cep_usuario = 'cep_usuario atualizado'
        tabela_inserida.telefone = 'telefone atualizado'
        resultado = colaborador_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = colaborador_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.funcao == "funcao atualizada", "A função atualizada não confere"
        assert dados_db.nome == "nome atualizado", "O nome atualizado não confere"
        assert dados_db.email == "email atualizado", "O email atualizado não confere"
        assert dados_db.senha == "senha atualizada", "A senha atualizada não confere"
        assert dados_db.cpf == "cpf atualizado", "O cpf atualizado não confere"
        assert dados_db.data_nascimento.strftime("%Y-%m-%d") == "2000-01-01", "A data de nascimento atualizada não confere"
        assert dados_db.status == False, "O status atualizado não confere"
        assert dados_db.data_cadastro.strftime("%Y-%m-%d") == "2000-01-01", "A data de cadastro não confere"
        assert dados_db.rua_usuario == "rua_usuario atualizada", "A rua atualizada não confere"
        assert dados_db.bairro_usuario == "bairro_usuario atualizado", "O bairro atualizado não confere"
        assert dados_db.cep_usuario == "cep_usuario atualizado", "O nome atualizado não confere"
        assert dados_db.telefone == "telefone atualizado", "O telefone atualizado não confere"

    def test_update_inexistente(self, test_db, colaborador_exemplo):
        #Arrange)
        usuario_repo.criar_tabela()

        colaborador_repo.criar_tabela()
        colaborador_exemplo.cod_colaborador = 999  # ID inexistente
        #Act
        resultado = colaborador_repo.update(colaborador_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, usuario_exemplo, cidade_exemplo, colaborador_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        colaborador_exemplo.cod_colaborador = id_usuario
        colaborador_repo.criar_tabela()
        id_tabela_inserida = colaborador_repo.inserir(colaborador_exemplo)                   
        #Act
        resultado = colaborador_repo.delete(id_tabela_inserida)
            
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = colaborador_repo.obter_por_id(id_tabela_inserida)     
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        usuario_repo.criar_tabela()        
        colaborador_repo.criar_tabela()
        #Act
        resultado = colaborador_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_colaboradores_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            for cidade in lista_cidades_exemplo:
                cidade_repo.inserir(cidade)
        
            usuario_repo.criar_tabela()
            for usuario in lista_usuarios_exemplo:
                usuario_repo.inserir(usuario, cursor)
            conn.commit()
        
        colaborador_repo.criar_tabela()
        for colaborador in lista_colaboradores_exemplo:
            colaborador_repo.inserir(colaborador)
        #Act
        dados_db = colaborador_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(c, Colaborador) for c in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = []
        for colaborador in dados_db:
            cod_esperados.append(colaborador.cod_colaborador)
        cod_retornados = [c.cod_colaborador for c in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_colaboradores_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            for cidade in lista_cidades_exemplo:
                cidade_repo.inserir(cidade)

            usuario_repo.criar_tabela()
            for usuario in lista_usuarios_exemplo:
                usuario_repo.inserir(usuario, cursor)
            conn.commit()

        colaborador_repo.criar_tabela()
        #Act
        dados_db = colaborador_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, usuario_exemplo, colaborador_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        colaborador_exemplo.cod_colaborador = id_usuario
        colaborador_repo.criar_tabela()
        id_tabela_inserida = colaborador_repo.inserir(colaborador_exemplo)
           
        #Act
        dados_db = colaborador_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "O Colaborador obtido não deveria ser None"
        assert dados_db.cod_colaborador == id_tabela_inserida, "O ID do colaborador inserido não confere"
        assert dados_db.funcao == "funcao teste", "A função inserida não confere"
        assert dados_db.cod_usuario == id_tabela_inserida, "O ID do plano inserido não confere"
        assert dados_db.nome == "nome teste", "O nome inserido não confere"
        assert dados_db.email == "email teste", "O email inserido não confere"
        assert dados_db.senha == "senha teste", "A senha inserida não confere"
        assert dados_db.cpf == "cpf teste", "O cpf inserido não confere"
        assert dados_db.data_nascimento.strftime("%Y-%m-%d") == "2025-01-01", "A data de nascimento inserida não confere"
        assert dados_db.status == True, "O status inserido não confere"
        assert dados_db.data_cadastro.strftime("%Y-%m-%d") == "2025-01-01", "A data de cadastro inserida não confere"
        assert dados_db.rua_usuario == "rua_usuario teste", "A rua_usuário inserida não confere"
        assert dados_db.bairro_usuario == "bairro_usuario teste", "O bairro do usuário inserido não confere"
        assert dados_db.cidade_usuario == id_cidade, "A cidade do usuário inserido não confere"
        assert dados_db.cep_usuario == "cep_usuario teste", "O cep do usuário inserido não confere"
        assert dados_db.telefone == "telefone teste", "O telefone inserido não confere"

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, usuario_exemplo, colaborador_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        colaborador_repo.criar_tabela()
        #Act
        dados_db = colaborador_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"