from data.repo import usuario_repo, doador_repo, cidade_repo
from data.model.doador_model import Doador
from data.util.database import get_connection

class TestDoadorRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        #Act
        resultado = doador_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, usuario_exemplo, doador_exemplo, cidade_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)
            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_repo.criar_tabela()
        doador_exemplo.cod_doador = id_usuario  
        # colaborador_exemplo.cod_usuario = id_usuario      
        #Act
        id_tabela_inserida = doador_repo.inserir(doador_exemplo)
        #Assert
        dados_db = doador_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "A assinatura inserida não deveria ser None"
        assert dados_db.cod_doador == id_tabela_inserida, "O ID do colaborador inserido não confere"
        assert dados_db.tipo_sanguineo == "tipo_sanguineo teste", "A função inserida não confere"
        assert dados_db.fator_rh == "fator_rh teste", "A função inserida não confere"
        assert dados_db.elegivel == "elegivel teste", "A função inserida não confere"
        assert dados_db.altura == 10.0, "A função inserida não confere"
        assert dados_db.peso == 10.0, "A função inserida não confere"
        assert dados_db.profissao == "profissao teste", "A função inserida não confere"
        assert dados_db.contato_emergencia == "contato_emergencia teste", "A função inserida não confere"
        assert dados_db.telefone_emergencia == "telefone_emergencia teste", "A função inserida não confere"
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


    def test_update_existente(self, test_db, usuario_exemplo, cidade_exemplo, doador_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_repo.criar_tabela()
        id_tabela_inserida = doador_repo.inserir(doador_exemplo)
        tabela_inserida = doador_repo.obter_por_id(id_tabela_inserida)          
        #Act
        #Lembrar que as chaves estrangeiras não podem ser atualizadas
        tabela_inserida.tipo_sanguineo = "tipo_sanguineo atualizado"
        tabela_inserida.fator_rh = "fator_rh atualizado"
        tabela_inserida.elegivel = "elegivel atualizado"
        tabela_inserida.altura = 10.0
        tabela_inserida.peso = 10.0
        tabela_inserida.profissao = "profissao teste"
        tabela_inserida.contato_emergencia = "contato_emergencia teste"
        tabela_inserida.telefone_emergencia = "telefone_emergencia teste"
        tabela_inserida.nome = "nome atualizado"
        tabela_inserida.email = "email atualizado"
        tabela_inserida.senha = "senha atualizado"
        tabela_inserida.cpf = "cpf atualizado"
        tabela_inserida.data_nascimento = "2000-01-01"
        tabela_inserida.status = False
        tabela_inserida.data_cadastro = "2000-01-01"
        tabela_inserida.rua_usuario = "rua_usuario atualizado"
        tabela_inserida.bairro_usuario = "bairro_usuario atualizado"
        tabela_inserida.cep_usuario = 'cep_usuario atualizado'
        tabela_inserida.telefone = 'telefone atualizado'
        resultado = doador_repo.update(tabela_inserida)
        #Assert
        assert resultado == True, "A atualização da assinatura deveria retornar True"
        dados_db = doador_repo.obter_por_id(id_tabela_inserida)
        assert dados_db.tipo_sanguineo == "tipo_sanguineo atualizado", "A função atualizada não confere"
        assert dados_db.fator_rh == "fator_rh atualizado", "A função atualizada não confere"
        assert dados_db.elegivel == "elegivel atualizado", "A função atualizada não confere"
        assert dados_db.altura == 10.0, "A função atualizada não confere"
        assert dados_db.peso == 10.0, "A função atualizada não confere"
        assert dados_db.profissao == "profissao teste", "A função atualizada não confere"
        assert dados_db.contato_emergencia == "contato_emergencia teste", "A função atualizada não confere"
        assert dados_db.telefone_emergencia == "telefone_emergencia teste", "A função atualizada não confere"
        assert dados_db.nome == "nome atualizado", "O nome atualizado não confere"
        assert dados_db.email == "email atualizado", "O email atualizado não confere"
        assert dados_db.senha == "senha atualizado", "A senha atualizada não confere"
        assert dados_db.cpf == "cpf atualizado", "O cpf atualizado não confere"
        assert dados_db.data_nascimento.strftime("%Y-%m-%d") == "2000-01-01", "A data de nascimento atualizada não confere"
        assert dados_db.status == False, "O status atualizado não confere"
        assert dados_db.data_cadastro.strftime("%Y-%m-%d") == "2000-01-01", "A data de cadastro não confere"
        assert dados_db.rua_usuario == "rua_usuario atualizado", "A rua atualizada não confere"
        assert dados_db.bairro_usuario == "bairro_usuario atualizado", "O bairro atualizado não confere"
        assert dados_db.cep_usuario == "cep_usuario atualizado", "O nome atualizado não confere"
        assert dados_db.telefone == "telefone atualizado", "O telefone atualizado não confere"

    def test_update_inexistente(self, test_db, doador_exemplo):
        #Arrange)
        cidade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        doador_repo.criar_tabela()
        doador_exemplo.cod_doador = 999  # ID inexistente
        #Act
        resultado = doador_repo.update(doador_exemplo)
        #Assert
        assert resultado == False, "A atualização de um id inexistente deveria retornar False"
        
    def test_delete_existente(self, test_db, usuario_exemplo, cidade_exemplo, doador_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_exemplo.cod_doador = id_usuario
        doador_repo.criar_tabela()
        id_tabela_inserida = doador_repo.inserir(doador_exemplo)                   
        #Act
        resultado = doador_repo.delete(id_tabela_inserida)
            
        #Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        tabela_excluida = doador_repo.obter_por_id(id_tabela_inserida)     
        assert tabela_excluida is None, "A assinatura não foi excluída corretamente, deveria ser None"

    def test_delete_inexistente(self, test_db):
        #Arrange
        cidade_repo.criar_tabela()
        usuario_repo.criar_tabela()        
        doador_repo.criar_tabela()
        #Act
        resultado = doador_repo.delete(999)  # ID inexistente
        #Assert
        assert resultado == False, "A exclusão de uma assinatura inexistente deveria retornar False"

    def test_obter_todos(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_doadores_exemplo):
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
        
        doador_repo.criar_tabela()
        for doador in lista_doadores_exemplo:
            doador_repo.inserir(doador)
        #Act
        dados_db = doador_repo.obter_todos()
        #Assert
        assert len(dados_db) == 10, "Deveria retornar 10 assinaturas"
        assert all(isinstance(c, Doador) for c in dados_db), "Todos os itens retornados deveriam ser do tipo Assinatura"
        cod_esperados = []
        for doador in dados_db:
            cod_esperados.append(doador.cod_doador)
        cod_retornados = [c.cod_doador for c in dados_db]
        assert cod_retornados == cod_esperados, "Os IDs das assinaturas retornadas deveriam ser de 1 a 10"     

    def test_obter_todos_vazia(self, test_db, lista_cidades_exemplo, lista_usuarios_exemplo, lista_doadores_exemplo):
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

        doador_repo.criar_tabela()
        #Act
        dados_db = doador_repo.obter_todos()
        #Assert
        assert isinstance(dados_db, list), "Deveria retornar uma lista"
        assert len(dados_db) == 0, "Deveria retornar uma lista vazia de cidades"

    def test_obter_por_id_existente(self, test_db, cidade_exemplo, usuario_exemplo, doador_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            id_cidade = cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            id_usuario = usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_exemplo.cod_doador = id_usuario
        doador_repo.criar_tabela()
        id_tabela_inserida = doador_repo.inserir(doador_exemplo)
           
        #Act
        dados_db = doador_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "O Colaborador obtido não deveria ser None"
        assert dados_db.cod_doador == id_tabela_inserida, "O ID do colaborador inserido não confere"
        assert dados_db.tipo_sanguineo == "tipo_sanguineo teste", "A função inserida não confere"
        assert dados_db.fator_rh == "fator_rh teste", "A função inserida não confere"
        assert dados_db.elegivel == "elegivel teste", "A função inserida não confere"
        assert dados_db.altura == 10.0, "A função inserida não confere"
        assert dados_db.peso == 10.0, "A função inserida não confere"
        assert dados_db.profissao == "profissao teste", "A função inserida não confere"
        assert dados_db.contato_emergencia == "contato_emergencia teste", "A função inserida não confere"
        assert dados_db.telefone_emergencia == "telefone_emergencia teste", "A função inserida não confere"
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

    def test_obter_por_id_inexistente(self, test_db, cidade_exemplo, usuario_exemplo, doador_exemplo):
        #Arrange
        with get_connection() as conn:
            cursor = conn.cursor()
            cidade_repo.criar_tabela()
            cidade_repo.inserir(cidade_exemplo)

            usuario_repo.criar_tabela()
            usuario_repo.inserir(usuario_exemplo, cursor)
            conn.commit()

        doador_repo.criar_tabela()
        #Act
        dados_db = doador_repo.obter_por_id(999)
        #Assert
        assert dados_db is None, "A assinatura obtida deveria ser None para um ID inexistente"