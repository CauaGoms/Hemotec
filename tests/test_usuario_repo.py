from data.repo import usuario_repo, cidade_repo
from data.model.usuario_model import Usuario
from data.util.database import get_connection
class TestUsuarioRepo:
    def test_criar_tabela_usuario(self, test_db):
        #Arrange
        #Act
        resultado = usuario_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, usuario_exemplo, cidade_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            #Act
            id_tabela_inserida = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()
            #Assert
        dados_db = usuario_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "O usuário inserido não deveria ser None"
        assert dados_db.cod_usuario == 1, "O ID do usuário inserido deveria ser igual a 1"
        assert dados_db.nome == "nome teste", "O nome do usuário inserida não confere"
        assert dados_db.email == "email teste", "O email do usuário inserido não confere"
        assert dados_db.senha == "senha teste", "A sigla do estado inserida não confere"
        assert dados_db.cpf == "cpf teste", "O CPF do usuário inserido não confere"
        assert dados_db.data_nascimento.strftime('%Y-%m-%d') == "2025-01-01", "A data de nascimento do usuário inserido não confere"
        assert dados_db.status == True, "O status do usuário inserido não confere"
        assert dados_db.data_cadastro.strftime('%Y-%m-%d') == "2025-01-01", "A data de cadastro do usuário inserido não confere"
        assert dados_db.rua_usuario == "rua_usuario teste", "A rua do usuário inserido não confere"
        assert dados_db.bairro_usuario == "bairro_usuario teste", "O bairro do usuário inserido não confere"
        assert dados_db.cidade_usuario == 1, "A cidade do usuário inserido não confere"
        assert dados_db.cep_usuario == "cep_usuario teste", "O CEP do usuário inserido não confere"
        assert dados_db.telefone == "telefone teste", "O telefone do usuário inserido não confere"


    def test_update_existente(self, test_db, usuario_exemplo, cidade_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_tabela_inserida = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()
            tabela_inserida = usuario_repo.obter_por_id(id_tabela_inserida)
            
        #Act
        tabela_inserida.cod_usuario = id_tabela_inserida
        tabela_inserida.nome = "nome atualizada"
        tabela_inserida.email = "email atualizada"
        tabela_inserida.senha = "senha atualizada"
        tabela_inserida.cpf = "cpf atualizado"
        tabela_inserida.data_nascimento = "2000-01-01"
        tabela_inserida.status = False
        tabela_inserida.data_cadastro = "2000-01-01"
        tabela_inserida.rua_usuario = "rua_usuario atualizada"
        tabela_inserida.bairro_usuario = "bairro_usuario atualizado"
        tabela_inserida.cep_usuario = "cep_usuario atualizado"
        tabela_inserida.telefone = "telefone atualizado"
        resultado = usuario_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização do usuário deveria retornar True"
        dados_db = usuario_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.nome == "nome atualizada", "O nome da cidade atualizada não confere"
        assert dados_db.email == "email atualizada", "A sigla do estado atualizada não confere"
        assert dados_db.senha == "senha atualizada", "A senha do usuário atualizado não confere"
        assert dados_db.cpf == "cpf atualizado", "O CPF do usuário atualizado não confere"
        assert dados_db.data_nascimento.strftime('%Y-%m-%d') == "2000-01-01", "A data de nascimento do usuário atualizado não confere"
        assert dados_db.status == False, "O status do usuário atualizado não confere"
        assert dados_db.data_cadastro.strftime('%Y-%m-%d') == "2000-01-01", "A data de cadastro do usuário atualizado não confere"
        assert dados_db.rua_usuario == "rua_usuario atualizada", "A rua do usuário atualizado não confere"
        assert dados_db.bairro_usuario == "bairro_usuario atualizado", "O bairro do usuário atualizado não confere"
        assert dados_db.cep_usuario == "cep_usuario atualizado", "O CEP do usuário atualizado não confere"
        assert dados_db.telefone == "telefone atualizado", "O telefone do usuário atualizado não confere"

    def test_update_inexistente(self, test_db, usuario_exemplo):
        #Arrange
        usuario_repo.criar_tabela()
        usuario_exemplo.cod_usuario = 999  # ID inexistente
        #Act
        resultado = usuario_repo.update(usuario_exemplo)
        #Assert
        assert resultado == False, "A atualização de um  inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, usuario_exemplo, cidade_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_tabela_inserida = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()        
        #Act
        resultado = usuario_repo.delete(id_tabela_inserida)
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = usuario_repo.obter_por_id(id_tabela_inserida)
        assert tabela_excluida is None, "A cidade não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        #Act
        resultado = usuario_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma cidade inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_usuarios_exemplo, lista_cidades_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        for cidade in lista_cidades_exemplo:
            cidade_repo.inserir(cidade)
        
        with get_connection() as conn:
            cursor = conn.cursor()
            usuario_repo.criar_tabela()
            for usuario in lista_usuarios_exemplo:
                usuario_repo.inserir(usuario, cursor)
            conn.commit()
        #Act
        dados_db = usuario_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 cidades"
        assert all(isinstance(u, Usuario) for u in dados_db), "Todos os itens retornados deveriam ser do tipo Usuario"
        cod_esperados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        cod_retornados = [u.cod_usuario for u in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs dos usuários retornados deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        for cidade in lista_cidades_exemplo:
            cidade_repo.inserir(cidade)

        usuario_repo.criar_tabela()
        #Act
        dados_db = usuario_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, usuario_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_tabela_inserida = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()
        #Act
        dados_db = usuario_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "A Cidade obtida não deveria ser None"
        assert dados_db.cod_usuario == id_tabela_inserida, "O ID da Cidade obtida deveria ser igual ao ID da cidade inserido"
        assert dados_db.nome == "nome teste", "O nome da Cidade obtida deveria ser igual ao nome da cidade inserido"
        assert dados_db.email == "email teste", "A sigla do estado obtida deveria ser igual a sigla do estado da cidade inserida"
        assert dados_db.senha == "senha teste", "A senha do usuário obtida deveria ser igual a senha do usuário inserido"
        assert dados_db.cpf == "cpf teste", "O CPF do usuário obtido deveria ser igual ao CPF do usuário inserido"
        assert dados_db.data_nascimento.strftime('%Y-%m-%d') == "2025-01-01", "A data de nascimento do usuário obtida deveria ser igual a data de nascimento do usuário inserido"
        assert dados_db.status == True, "O status do usuário obtido deveria ser igual ao status do usuário inserido"
        assert dados_db.data_cadastro.strftime('%Y-%m-%d') == "2025-01-01", "A data de cadastro do usuário obtida deveria ser igual a data de cadastro do usuário inserido"
        assert dados_db.rua_usuario == "rua_usuario teste", "A rua do usuário obtida deveria ser igual a rua do usuário inserido"
        assert dados_db.bairro_usuario == "bairro_usuario teste", "O bairro do usuário obtida deveria ser igual ao bairro do usuário inserido"
        assert dados_db.cidade_usuario == 1, "A cidade do usuário obtida deveria ser igual a cidade do usuário inserido"
        assert dados_db.cep_usuario == "cep_usuario teste", "O CEP do usuário obtida deveria ser igual ao CEP do usuário inserido"
        assert dados_db.telefone == "telefone teste", "O telefone do usuário obtida deveria ser igual ao telefone do usuário inserido"

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)
        usuario_repo.criar_tabela()
        #Act
        dados_db = usuario_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A Cidade obtida deveria ser None para um ID inexistente"
    
    def test_obter_por_email_existente(self, test_db, cidade_exemplo, usuario_exemplo):
        pass