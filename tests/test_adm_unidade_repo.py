from data.repo import adm_unidade_repo, assinatura_repo, cidade_repo, instituicao_repo, licenca_repo, plano_repo, unidade_coleta_repo, usuario_repo
from data.model.adm_unidade_model import Adm_unidade
from data.util.database import get_connection
from tests.conftest import cidade_exemplo
class TestAdm_UnidadeRepo:
    def test_criar_tabela_usuario(self, test_db):
        #Arrange
        #Act
        resultado = adm_unidade_repo.criar_tabela()
        #Assert
        assert resultado == True, "A criação da tabela deveria retornar True"
