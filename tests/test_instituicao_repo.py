from data.repo import instituicao_repo, cidade_repo, gestor_repo, assinatura_repo, usuario_repo

class TestInstituicaoRepo:
    def test_criar_tabela_instituicao(self, test_db):
        #Arrange
        #Act
        resultado = instituicao_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir(self, test_db, instituicao_exemplo, cidade_exemplo, gestor_exemplo, assinatura_exemplo, usuario_exemplo):
        #Arrange
        cidade_repo.criar_tabela()
        cidade_repo.inserir(cidade_exemplo)

        usuario_repo.criar_tabela()
        usuario_repo.inserir(usuario_exemplo, None)

        gestor_repo.criar_tabela()
        gestor_repo.inserir(gestor_exemplo)

        assinatura_repo.criar_tabela()
        assinatura_repo.inserir(assinatura_exemplo)

        instituicao_repo.criar_tabela()
        #Act
        id_tabela_inserida = instituicao_repo.inserir(instituicao_exemplo)
        #Assert
        dados_db = instituicao_repo.obter_por_id(id_tabela_inserida)
        assert dados_db is not None, "A instituição inserida não deveria ser None"
        assert dados_db.cnpj == "cnpj teste", "O ID da instituição inserida deveria ser igual a cnpj teste"
        assert dados_db.cod_gestor == 1, "O código do gestor da instituição inserida não confere"
        assert dados_db.cod_assinatura == 1, "O código da assinatura da instituição inserida não confere"
        assert dados_db.nome == "nome teste", "O nome da instituição inserida não confere"
        assert dados_db.email == "email teste", "O email da instituição inserido não confere"
        assert dados_db.rua_instituicao == "rua_instituicao teste", "A rua da instituição inserida não confere"
        assert dados_db.bairro_instituicao == "bairro_instituicao teste", "O bairro da instituição inserida não confere"
        assert dados_db.cidade_instituicao == 1, "A cidade da instituição inserida não confere"
        assert dados_db.cep_instituicao == "cep_instituicao teste", "O CEP da instituição inserida não confere"
        assert dados_db.telefone == "telefone teste", "O telefone da instituição inserida não confere"