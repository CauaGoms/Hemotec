from data.repo import gestor_repo, usuario_repo, instituicao_repo, cidade_repo, assinatura_repo

class TestGestorRepo:
    def test_criar_tabela_gestor(self, test_db):
        #Arrange
        #Act
        resultado = gestor_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_obter_por_id_existente(self, test_db, gestor_exemplo, usuario_exemplo, instituicao_exemplo, cidade_exemplo ,assinatura_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        plano_repo = criar_tabela()
        plano_repo.inserir(plano_exemplo)

        assinatura_repo.criar_tabela()
        assinatura_repo.inserir(assinatura_exemplo)

        instituicao_repo.criar_tabela()
        instituicao_repo.inserir(instituicao_exemplo)

        usuario_repo.criar_tabela()
        usuario_repo.inserir(usuario_exemplo)

        gestor_repo.criar_tabela()
        id_tabela_inserida = gestor_repo.inserir(gestor_exemplo)

        #Act
        dados_db = gestor_repo.obter_por_id(id_tabela_inserida)
        #Assert
        assert dados_db is not None, "O Gestor obtido não deveria ser None"
        assert dados_db.cod_gestor == id_tabela_inserida, "O ID da Cidade obtida deveria ser igual ao ID da cidade inserido"
        assert dados_db.nome == "nome teste", "O nome do gestor obtido deveria ser igual ao nome do gestor inserido"
        assert dados_db.email == "email teste", "O email obtido deveria ser igual ao email inserido"
        assert dados_db.senha == "senha teste", "A senha obtida deveria ser igual a senha inserida"
        assert dados_db.cpf == "cpf teste", "O CPF obtido deveria ser igual ao CPF inserido"
        assert dados_db.data_nascimento.strftime("%Y-%m-%d") == "2025-01-01", "A data de nascimento obtida deveria ser igual a data de nascimento inserida"
        assert dados_db.status == True, "O status obtido deveria ser igual ao status inserido"
        assert dados_db.data_cadastro.strftime("%Y-%m-%d") == "2025-01-01", "A data de cadastro obtida deveria ser igual a data de cadastro inserida"
        assert dados_db.rua_usuario == "rua_usuario teste", "A rua do gestor obtida deveria ser igual a rua do gestor inserido"
        assert dados_db.bairro_usuario == "bairro_usuario teste", "O bairro do gestor obtido deveria ser igual ao bairro do gestor inserido"
        assert dados_db.cidade_usuario == 1, "A cidade do gestor obtida deveria ser igual a cidade do gestor inserido"
        assert dados_db.cep_usuario == "cep_usuario teste", "O CEP do gestor obtido deveria ser igual ao CEP do gestor inserido"
        assert dados_db.telefone == "telefone teste", "O telefone do gestor obtido deveria ser igual ao telefone do gestor inserido"
        assert dados_db.cnpj == "cnpj teste", "O CNPJ do gestor obtido deveria ser igual ao CNPJ do gestor inserido"
        assert dados_db.instituicao == "instituicao teste", "A instituição do gestor obtida deveria ser igual a instituição do gestor inserido"
    