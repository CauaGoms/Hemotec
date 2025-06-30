from datetime import datetime 
import pytest
import os
import sys
import tempfile

# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Fixture para criar um banco de dados temporário para testes
@pytest.fixture
def test_db():
    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    # Configura a variável de ambiente para usar o banco de teste
    os.environ['TEST_DATABASE_PATH'] = db_path
    # Retorna o caminho do banco de dados temporário
    yield db_path    
    # Remove o arquivo temporário ao concluir o teste
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def cidade_exemplo():
    from data.model.cidade_model import Cidade
    cidade = Cidade(0, "nome_cidade teste", "sigla_estado teste")
    return cidade

@pytest.fixture
def lista_cidades_exemplo():
    from data.model.cidade_model import Cidade
    cidades = []
    for i in range(1, 11):
        cidade = Cidade(0, f'nome_cidade {i:02d}', f'sigla_estado {i:02d}')
        cidades.append(cidade)
    return cidades

@pytest.fixture
def campanha_exemplo():
    from data.model.campanha_model import Campanha
    campanha = Campanha(0, "titulo teste", "descricao teste", datetime(2025, 1, 1).date(), datetime(2025, 1, 1).date(), "status teste")
    return campanha

@pytest.fixture
def lista_campanhas_exemplo():
    from data.model.campanha_model import Campanha
    campanhas = []
    for i in range(1, 11):
        campanha = Campanha(0, f'titulo {i:02d}', f'descricao {i:02d}', datetime(2025, 1, i).date(), datetime(2025, 1, i).date(), f"status {i:02d}")
        campanhas.append(campanha)
    return campanhas

@pytest.fixture
def usuario_exemplo():
    from data.model.usuario_model import Usuario
    usuario = Usuario(0, "nome teste", "email teste", "senha teste", "cpf teste", datetime(2025, 1, 1).date(), True, datetime(2025, 1, 1).date(), "rua_usuario teste", "bairro_usuario teste", 1, "cep_usuario teste","telefone teste"
    )
    return usuario

@pytest.fixture
def lista_usuarios_exemplo():
    from data.model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(
            0,
            f'nome {i:02d}',
            f'email {i:02d}',
            f'senha {i:02d}',
            f'cpf {i:02d}',
            datetime(2025, 1, i).date(),
            True,
            datetime(2025, 1, i).date(),
            f'rua_usuario {i:02d}',
            f'bairro_usuario {i:02d}',
            i,  # Supondo que a cidade tenha o ID igual ao índice
            f'cep_usuario {i:02d}',
            f'telefone {i:02d}'
        )
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def gestor_exemplo():
    from data.model.gestor_model import Gestor
    gestor = Gestor(
        1,
        0,
        "nome teste",
        "email teste",
        "senha teste",
        "cpf teste",
        datetime(2025, 1, 1).date(),
        True,
        datetime(2025, 1, 1).date(),
        "rua_usuario teste",
        "bairro_usuario teste",
        1, 
        "cep_usuario teste",
        "telefone teste",
        "cnpj teste",
        "instituicao teste"
    )
    return gestor

@pytest.fixture
def lista_gestores_exemplo():
    from data.model.gestor_model import Gestor
    gestores = []
    for i in range(1, 11):
        gestor = Gestor(
            i,
            f'nome {i:02d}',
            f'email {i:02d}',
            f'senha {i:02d}',
            f'cpf {i:02d}',
            datetime(2025, 1, i).date(),
            True,
            datetime(2025, 1, i).date(),
            f'rua_gestor {i:02d}',
            f'bairro_gestor {i:02d}',
            i,  # Supondo que a cidade tenha o ID igual ao índice
            f'cep_gestor {i:02d}',
            f'telefone {i:02d}',
            f'cnpj {i:02d}',
            f'instituicao {i:02d}'
        )
        gestores.append(gestor)
    return gestores

@pytest.fixture
def instituicao_exemplo():
    from data.model.instituicao_model import Instituicao
    instituicao = Instituicao(
        "cnpj teste", 
        1, 
        1,
        "nome teste",
        "email teste",
        "rua_instituicao teste",
        "bairro_instituicao teste",
        1,
        "cep_instituicao teste",
        "telefone teste"
        )
    return instituicao

@pytest.fixture
def lista_instituicoes_exemplo():
    from data.model.instituicao_model import Instituicao
    instituicoes = []
    for i in range(1, 11):
        instituicao = Instituicao(
            f'cnpj {i:02d}', 
            i, 
            i,
            f'nome {i:02d}',
            f'email {i:02d}',
            f'rua_instituicao {i:02d}',
            f'bairro_instituicao {i:02d}',
            i,
            f'cep_instituicao {i:02d}',
            f'telefone {i:02d}'
        )
        instituicoes.append(instituicao)
    return instituicoes

@pytest.fixture
def assinatura_exemplo():
    from data.model.assinatura_model import Assinatura
    assinatura = Assinatura(
        1,
        "cnpj teste",
        1,
        1,
        datetime(2025, 1, 1).date(),
        datetime(2025, 1, 1).date(),
        10.0,
        10
    )
    return assinatura

@pytest.fixture
def lista_assinaturas_exemplo():
    pass