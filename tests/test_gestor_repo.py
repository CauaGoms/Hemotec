from data.repo import gestor_repo, usuario_repo, instituicao_repo, cidade_repo
from data.model.gestor_model import Gestor
from data.util.database import get_connection

class TestGestorRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = gestor_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, gestor_exemplo, usuario_exemplo, instituicao_exemplo, cidade_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        instituicao_repo.criar_tabela()
        id_instituicao = instituicao_repo.inserir(instituicao_exemplo)
        gestor_repo.criar_tabela()
        gestor_exemplo.cod_gestor = id_usuario
        #Act
        id_tabela_inserida = gestor_repo.inserir(gestor_exemplo)
        #Assert
        dados_db = gestor_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "O Gestor obtido não deveria ser None"
        assert dados_db.cod_gestor == id_tabela_inserida, "O ID da Cidade obtida deveria ser igual ao ID da cidade inserido"
        assert dados_db.instituicao == "instituicao teste", "A instituição do gestor obtida deveria ser igual a instituição do gestor inserido"
        assert dados_db.cod_instituicao == id_instituicao, "A instituição do gestor obtida deveria ser igual a instituição do gestor inserido"
        assert dados_db.cod_usuario == id_tabela_inserida, "O ID do plano inserido não confere"
        assert dados_db.nome == "nome teste", "O nome do gestor obtido deveria ser igual ao nome do gestor inserido"
        assert dados_db.email == "email teste", "O email obtido deveria ser igual ao email inserido"
        assert dados_db.senha == "senha teste", "A senha obtida deveria ser igual a senha inserida"
        assert dados_db.cpf == "cpf teste", "O CPF obtido deveria ser igual ao CPF inserido"
        assert dados_db.data_nascimento.strftime("%Y-%m-%d") == "2025-01-01", "A data de nascimento obtida deveria ser igual a data de nascimento inserida"
        assert dados_db.status == True, "O status obtido deveria ser igual ao status inserido"
        assert dados_db.data_cadastro.strftime("%Y-%m-%d") == "2025-01-01", "A data de cadastro obtida deveria ser igual a data de cadastro inserida"
        assert dados_db.rua_usuario == "rua_usuario teste", "A rua do gestor obtida deveria ser igual a rua do gestor inserido"
        assert dados_db.bairro_usuario == "bairro_usuario teste", "O bairro do gestor obtido deveria ser igual ao bairro do gestor inserido"
        assert dados_db.cidade_usuario == id_cidade, "A cidade do gestor obtida deveria ser igual a cidade do gestor inserido"
        assert dados_db.cep_usuario == "cep_usuario teste", "O CEP do gestor obtido deveria ser igual ao CEP do gestor inserido"
        assert dados_db.telefone == "telefone teste", "O telefone do gestor obtido deveria ser igual ao telefone do gestor inserido"
        
    def test_update_existente(self, test_db, usuario_exemplo, cidade_exemplo, instituicao_exemplo, gestor_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)
            
            usuario_repo.criar_tabela()
            usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)
        gestor_repo.criar_tabela()
        id_tabela_inserida = gestor_repo.inserir(gestor_exemplo)
        tabela_inserida = gestor_repo.obter_por_id(id_tabela_inserida)
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.instituicao = "instituicao atualizada"
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
        resultado = gestor_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = gestor_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.instituicao == "instituicao atualizada", "A função atualizada não confere"
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

    def test_update_inexistente(self, test_db, gestor_exemplo):
        #Arrange
        usuario_repo.criar_tabela()
        instituicao_repo.criar_tabela()
        gestor_repo.criar_tabela()
        gestor_exemplo.cod_gestor = 999  # ID inexistente
        #Act
        resultado = gestor_repo.update(gestor_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"

    def test_delete_existente(self, test_db, usuario_exemplo, cidade_exemplo, instituicao_exemplo, gestor_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)
            
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)
        gestor_exemplo.cod_gestor = id_usuario
        gestor_repo.criar_tabela()
        id_tabela_inserida = gestor_repo.inserir(gestor_exemplo)                   
        #Act
        resultado = gestor_repo.delete(id_tabela_inserida)
            
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = gestor_repo.obter_por_id(id_tabela_inserida)     
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        instituicao_repo.criar_tabela()
        gestor_repo.criar_tabela()
        #Act
        resultado = gestor_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_gestores_exemplo, lista_instituicoes_exemplo):
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

        instituicao_repo.criar_tabela()
        for instituicao in lista_instituicoes_exemplo:
            instituicao_repo.inserir(instituicao)
        
        gestor_repo.criar_tabela()
        for gestor in lista_gestores_exemplo:
            gestor_repo.inserir(gestor)
        #Act
        dados_db = gestor_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(g, Gestor) for g in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = []
        for gestor in dados_db:
            cod_esperados.append(gestor.cod_gestor)
        cod_retornados = [g.cod_gestor for g in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_instituicoes_exemplo, lista_gestores_exemplo):
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

        instituicao_repo.criar_tabela()
        for instituicao in lista_instituicoes_exemplo:
            instituicao_repo.inserir(instituicao)

        gestor_repo.criar_tabela()
        #Act
        dados_db = gestor_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, usuario_exemplo, instituicao_exemplo, gestor_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        instituicao_repo.criar_tabela()
        id_instituicao = instituicao_repo.inserir(instituicao_exemplo)

        gestor_exemplo.cod_gestor = id_usuario
        gestor_repo.criar_tabela()
        id_tabela_inserida = gestor_repo.inserir(gestor_exemplo)
           
        #Act
        dados_db = gestor_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "O Colaborador obtido não deveria ser None"
        assert dados_db.cod_gestor == id_tabela_inserida, "O ID do colaborador inserido não confere"
        assert dados_db.cod_instituicao == id_instituicao, "A função inserida não confere"
        assert dados_db.instituicao == "instituicao teste", "A função inserida não confere"
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
    
    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, usuario_exemplo, instituicao_exemplo, gestor_exemplo):
        #Arrange        
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)
            
            usuario_repo.criar_tabela()
            usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)
        gestor_repo.criar_tabela()
        #Act
        dados_db = gestor_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"