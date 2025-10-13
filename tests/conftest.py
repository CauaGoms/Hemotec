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
    cidade = Cidade(
        cod_cidade=0, 
        nome_cidade="nome_cidade teste", 
        sigla_estado="sigla_estado teste")
    return cidade

@pytest.fixture
def lista_cidades_exemplo():
    from data.model.cidade_model import Cidade
    cidades = []
    for i in range(1, 11):
        cidade = Cidade(
            cod_cidade=0, 
            nome_cidade=f'nome_cidade {i:02d}', 
            sigla_estado=f'sigla_estado {i:02d}')
        cidades.append(cidade)
    return cidades

@pytest.fixture
def campanha_exemplo():
    from data.model.campanha_model import Campanha
    campanha = Campanha(
        cod_campanha=0, 
        titulo="titulo teste", 
        descricao="descricao teste", 
        data_inicio=datetime(2025, 1, 1).date(), 
        data_fim=datetime(2025, 1, 1).date(), 
        status="status teste")
    return campanha

@pytest.fixture
def lista_campanhas_exemplo():
    from data.model.campanha_model import Campanha
    campanhas = []
    for i in range(1, 11):
        campanha = Campanha(
            cod_campanha=0, 
            titulo=f'titulo {i:02d}', 
            descricao=f'descricao {i:02d}', 
            data_inicio=datetime(2025, 1, i).date(), 
            data_fim=datetime(2025, 1, i).date(), 
            status=f"status {i:02d}")
        campanhas.append(campanha)
    return campanhas

@pytest.fixture
def usuario_exemplo():
    from data.model.usuario_model import Usuario
    usuario = Usuario(
        cod_usuario=0, 
        nome="nome teste", 
        email="email teste", 
        senha="senha teste", 
        cpf="cpf teste", 
        data_nascimento=datetime(2025, 1, 1).date(), 
        status=True, 
        data_cadastro=datetime(2025, 1, 1).date(),
        rua_usuario="rua_usuario teste", 
        bairro_usuario="bairro_usuario teste", 
        cidade_usuario=1, 
        cep_usuario="cep_usuario teste",
        telefone="telefone teste"
    )
    return usuario

@pytest.fixture
def lista_usuarios_exemplo():
    from data.model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(
            cod_usuario=0,
            nome=f'nome {i:02d}',
            email=f'email {i:02d}',
            senha=f'senha {i:02d}',
            cpf=f'cpf {i:02d}',
            data_nascimento=datetime(2025, 1, i).date(),
            status=True,  # Status alternando entre True e False
            data_cadastro=datetime(2025, 1, i).date(),
            rua_usuario=f'rua_usuario {i:02d}',
            bairro_usuario=f'bairro_usuario {i:02d}',
            cidade_usuario=i,  # Supondo que a cidade tenha o ID igual ao índice
            cep_usuario=f'cep_usuario {i:02d}',
            telefone=f'telefone {i:02d}'
        )
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def gestor_exemplo():
    from data.model.gestor_model import Gestor
    gestor = Gestor(
        cod_gestor=0,
        cod_instituicao=1,
        instituicao="instituicao teste",
        cod_usuario=1,
        nome="nome teste",
        email="email teste",
        senha="senha teste",
        cpf="cpf teste",
        data_nascimento=datetime(2025, 1, 1).date(),
        status=True,
        data_cadastro=datetime(2025, 1, 1).date(),
        rua_usuario="rua_usuario teste",
        bairro_usuario="bairro_usuario teste",
        cidade_usuario=1,
        cep_usuario="cep_usuario teste",
        telefone="telefone teste"
    )
    return gestor

@pytest.fixture
def lista_gestores_exemplo():
    from data.model.gestor_model import Gestor
    gestores = []
    for i in range(1, 11):
        gestor = Gestor(
            cod_usuario=i,
            nome=f'nome {i:02d}',
            email=f'email {i:02d}',
            senha=f'senha {i:02d}',
            cpf=f'cpf {i:02d}',
            data_nascimento=datetime(2025, 1, i).date(),
            status=True,
            data_cadastro=datetime(2025, 1, i).date(),
            rua_usuario=f'rua_usuario {i:02d}',
            bairro_usuario='bairro_usuario {i:02d}',
            cidade_usuario=i,  # Supondo que a cidade tenha o ID igual ao índice
            cep_usuario=f'cep_usuario {i:02d}',
            telefone=f'telefone {i:02d}',
            cod_gestor=i,
            cod_instituicao=i,
            instituicao=f'instituicao {i:02d}'
        )
        gestores.append(gestor)
    return gestores

@pytest.fixture
def instituicao_exemplo():
    from data.model.instituicao_model import Instituicao
    instituicao = Instituicao(
        cod_instituicao=0,
        cnpj="cnpj teste", 
        nome="nome teste",
        email="email teste",
        rua_instituicao="rua_instituicao teste",
        bairro_instituicao="bairro_instituicao teste",
        cidade_instituicao=1,
        cep_instituicao="cep_instituicao teste",
        telefone="telefone teste"
        )
    return instituicao

@pytest.fixture
def lista_instituicoes_exemplo():
    from data.model.instituicao_model import Instituicao
    instituicoes = []
    for i in range(1, 11):
        instituicao = Instituicao(
            cod_instituicao=0,
            cnpj=f'cnpj {i:02d}', 
            nome=f'nome {i:02d}',
            email=f'email {i:02d}',
            rua_instituicao=f'rua_instituicao {i:02d}',
            bairro_instituicao=f'bairro_instituicao {i:02d}',
            cidade_instituicao=i,
            cep_instituicao=f'cep_instituicao {i:02d}',
            telefone=f'telefone {i:02d}'
        )
        instituicoes.append(instituicao)
    return instituicoes

@pytest.fixture
def assinatura_exemplo():
    from data.model.assinatura_model import Assinatura
    assinatura = Assinatura(
        cod_assinatura=0,
        cod_instituicao=1,
        cod_plano=1,
        data_inicio=datetime(2025, 1, 1).date(),
        data_fim=datetime(2025, 1, 1).date(),
        valor=10.0,
        qtd_licenca=10
    )
    return assinatura

@pytest.fixture
def lista_assinaturas_exemplo():
    from data.model.assinatura_model import Assinatura
    assinaturas = []
    for i in range(1, 11):
        assinatura = Assinatura(
            cod_assinatura=0,
            cod_instituicao=i,
            cod_plano=i,
            data_inicio=datetime(2025, 1, i).date(),
            data_fim=datetime(2025, 1, i).date(),
            valor=float(i * 10),
            qtd_licenca=i * 10
        )
        assinaturas.append(assinatura)
    return assinaturas

@pytest.fixture
def plano_exemplo():
    from data.model.plano_model import Plano
    plano = Plano(
        cod_plano=1,
        qtd_licenca=10,
        nome="nome teste",
        valor=10.0,
        validade=10
    )
    return plano

@pytest.fixture
def lista_planos_exemplo():
    from data.model.plano_model import Plano
    planos = []
    for i in range(1, 11):
        plano = Plano(
            cod_plano=i,
            qtd_licenca=i * 10,
            nome=f'nome {i:02d}',
            valor=float(i * 10),
            validade=i * 10
        )
        planos.append(plano)
    return planos

@pytest.fixture
def licenca_exemplo():
    from data.model.licenca_model import Licenca
    licenca = Licenca(
        cod_licenca=1,
        cod_assinatura=1,
        status=1
    )
    return licenca

@pytest.fixture
def lista_licencas_exemplo():
    from data.model.licenca_model import Licenca
    licencas = []
    for i in range(1, 11):
        licenca = Licenca(
            cod_licenca=i,
            cod_assinatura=i,
            status=i 
        )
        licencas.append(licenca)
    return licencas

@pytest.fixture
def adm_unidade_exemplo():
    from data.model.adm_unidade_model import Adm_unidade
    adm_unidade = Adm_unidade(
        cod_usuario=0,
        nome="nome teste",
        email="email teste",
        senha="senha teste",
        cpf="cpf teste",
        data_nascimento=datetime(2025, 1, 1).date(),
        status=True,
        data_cadastro=datetime(2025, 1, 1).date(),
        rua_usuario="rua_usuario teste",
        bairro_usuario="bairro_usuario teste",
        cidade_usuario=1,
        cep_usuario="cep_usuario teste",
        telefone="telefone teste",
        cod_adm=1,
        cod_unidade=1,
        permissao_envio_campanha=True,
        permissao_envio_notificacao=True
    )
    return adm_unidade

@pytest.fixture
def lista_adm_unidades_exemplo():
    from data.model.adm_unidade_model import Adm_unidade
    adm_unidades = []
    for i in range(1, 11):
        adm_unidade = Adm_unidade(
            cod_usuario=i,
            cod_adm=i,
            cod_unidade=i,
            permissao_envio_campanha=True,
            permissao_envio_notificacao=True,
            nome=f'nome {i:02d}',
            email=f'email {i:02d}',
            senha=f'senha {i:02d}',
            cpf=f'cpf {i:02d}',
            data_nascimento=datetime(2025, 1, i).date(),
            status=True,
            data_cadastro=datetime(2025, 1, i).date(),
            rua_usuario=f'rua_usuario {i:02d}',
            bairro_usuario=f'bairro_usuario {i:02d}',
            cidade_usuario=i,
            cep_usuario=f'cep_usuario {i:02d}',
            telefone=f'telefone {i:02d}'
        )
        adm_unidades.append(adm_unidade)
    return adm_unidades

@pytest.fixture
def adm_campanha_exemplo():
    from data.model.adm_campanha_model import Adm_campanha
    adm_campanha = Adm_campanha(
        cod_adm=1,
        cod_campanha=1,
        papel="papel teste"
    )
    return adm_campanha

@pytest.fixture
def lista_adm_campanhas_exemplo():
    from data.model.adm_campanha_model import Adm_campanha
    adm_campanhas = []
    for i in range(1, 11):
        adm_campanha = Adm_campanha(
            cod_adm=i,
            cod_campanha=i,
            papel=f'papel {i:02d}'
        )
        adm_campanhas.append(adm_campanha)
    return adm_campanhas

@pytest.fixture
def unidade_coleta_exemplo():
    from data.model.unidade_coleta_model import Unidade_coleta
    unidade_coleta = Unidade_coleta(
        cod_unidade=0,
        cod_licenca=1,
        nome="nome teste",
        email="email teste",
        rua_unidade="rua_unidade teste",
        bairro_unidade="bairro_unidade teste",
        cidade_unidade=1,
        cep_unidade="cep_unidade teste",
        latitude=10.0,
        longitude=10.0,
        telefone="telefone teste"
    )
    return unidade_coleta

@pytest.fixture
def lista_unidades_coleta_exemplo():
    from data.model.unidade_coleta_model import Unidade_coleta
    unidades_coleta = []
    for i in range(1, 11):
        unidade_coleta = Unidade_coleta(
            cod_unidade=i,
            cod_licenca=i,
            nome=f'nome {i:02d}',
            email=f'email {i:02d}',
            rua_unidade=f'rua_unidade {i:02d}',
            bairro_unidade=f'bairro_unidade {i:02d}',
            cidade_unidade=i,
            cep_unidade=f'cep_unidade {i:02d}',
            latitude=float(i * 10),
            longitude=float(i * 10),
            telefone=f'telefone {i:02d}'
        )
        unidades_coleta.append(unidade_coleta)
    return unidades_coleta

@pytest.fixture
def estoque_exemplo():
    from data.model.estoque_model import Estoque
    estoque = Estoque(
        cod_estoque=1,
        cod_unidade=1,
        tipo_sanguineo="tipo_sanguineo teste",
        fator_rh="fator_rh teste",
        quantidade=10,
        data_atualizacao=datetime(2025, 1, 1).date()
    )
    return estoque

@pytest.fixture
def lista_estoques_exemplo():
    from data.model.estoque_model import Estoque
    estoques = []
    for i in range(1, 11):
        estoque = Estoque(
            cod_estoque=i,
            cod_unidade=i,
            tipo_sanguineo=f'tipo_sanguineo {i:02d}',
            fator_rh=f'fator_rh {i:02d}',
            quantidade=i * 10,
            data_atualizacao=datetime(2025, 1, i).date()
        )
        estoques.append(estoque)
    return estoques

@pytest.fixture
def notificacao_exemplo():
    from data.model.notificacao_model import Notificacao
    notificacao = Notificacao(
        cod_notificacao=1,
        cod_adm=1,
        tipo="tipo teste",
        mensagem="mensagem teste",
        status=1,
        data_envio=datetime(2025, 1, 1).date()
    )
    return notificacao

@pytest.fixture
def lista_notificacoes_exemplo():
    from data.model.notificacao_model import Notificacao
    notificacoes = []
    for i in range(1, 11):
        notificacao = Notificacao(
            cod_notificacao=i,
            cod_adm=i,
            tipo=f'tipo {i:02d}',
            mensagem=f'mensagem {i:02d}',
            status=i,
            data_envio=datetime(2025, 1, i).date()
        )
        notificacoes.append(notificacao)
    return notificacoes

@pytest.fixture
def colaborador_exemplo():
    from data.model.colaborador_model import Colaborador
    colaborador = Colaborador(
        cod_colaborador=0,
        funcao="funcao teste",
        nome="nome teste",
        email="email teste",
        senha="senha teste",
        cpf="cpf teste",
        data_nascimento=datetime(2025, 1, 1).date(),
        status=True,
        data_cadastro=datetime(2025, 1, 1).date(),
        rua_usuario="rua_usuario teste",
        bairro_usuario="bairro_usuario teste",
        cidade_usuario=1,
        cep_usuario="cep_usuario teste",
        telefone="telefone teste",
        cod_usuario=1
    )
    return colaborador

@pytest.fixture
def lista_colaboradores_exemplo():
    from data.model.colaborador_model import Colaborador
    colaboradores = []
    for i in range(1, 11):
        colaborador = Colaborador(
            cod_colaborador=i,
            funcao=f'funcao {i:02d}',
            cod_usuario=i,
            nome=f'nome {i:02d}',
            email=f'email {i:02d}',
            senha=f'senha {i:02d}',
            cpf=f'cpf {i:02d}',
            data_nascimento=datetime(2025, 1, i).date(),
            status=True,
            data_cadastro=datetime(2025, 1, i).date(),
            rua_usuario=f'rua_usuario {i:02d}',
            bairro_usuario=f'bairro_usuario {i:02d}',
            cidade_usuario=i,
            cep_usuario=f'cep_usuario {i:02d}',
            telefone=f'telefone {i:02d}'
        )
        colaboradores.append(colaborador)
    return colaboradores

@pytest.fixture
def agendamento_exemplo():
    from data.model.agendamento_model import Agendamento
    agendamento = Agendamento(
        cod_agendamento=0,
        cod_colaborador=1,
        cod_doador=1,
        data_hora=datetime(2025, 1, 1, 1, 0, 0),
        status=1,
        observacoes="observacoes teste",
        tipo_agendamento="tipo_agendamento teste"
    )
    return agendamento

@pytest.fixture
def lista_agendamentos_exemplo():
    from data.model.agendamento_model import Agendamento
    agendamentos = []
    for i in range(1, 11):
        agendamento = Agendamento(
            cod_agendamento=i,
            cod_colaborador=i,
            cod_doador=i,
            data_hora=datetime(2025, 1, i, i, 0, 0),
            status=i,
            observacoes=f'observacoes {i:02d}',
            tipo_agendamento=f'tipo_agendamento {i:02d}'
        )
        agendamentos.append(agendamento)
    return agendamentos

@pytest.fixture
def doador_exemplo():
    from data.model.doador_model import Doador
    doador = Doador(
        cod_doador=0,
        tipo_sanguineo="tipo_sanguineo teste",
        fator_rh="fator_rh teste",
        elegivel="elegivel teste",
        altura=10.0,
        peso=10.0,
        profissao="profissao teste",
        contato_emergencia="contato_emergencia teste",
        telefone_emergencia="telefone_emergencia teste",
        cod_usuario=1,
        nome="nome teste",
        email="email teste",
        senha="senha teste",
        cpf="cpf teste",
        data_nascimento=datetime(2025, 1, 1).date(),
        status=True,
        data_cadastro=datetime(2025, 1, 1).date(),
        rua_usuario="rua_usuario teste",
        bairro_usuario="bairro_usuario teste",
        cidade_usuario=1,
        cep_usuario="cep_usuario teste",
        telefone="telefone teste"
    )
    return doador

@pytest.fixture
def lista_doadores_exemplo():
    from data.model.doador_model import Doador
    doadores = []
    for i in range(1, 11):
        doador = Doador(
            cod_doador=i,
            tipo_sanguineo=f'tipo_sanguineo {i:02d}',
            fator_rh=f'fator_rh {i:02d}',
            elegivel=f'elegivel {i:02d}',
            altura=float(i * 10),
            peso=float(i * 10),
            profissao=f'profissao {i:02d}',
            contato_emergencia=f'contato_emergencia {i:02d}',
            telefone_emergencia=f'telefone_emergencia {i:02d}',
            cod_usuario=i,
            nome=f'nome {i:02d}',
            email=f'email {i:02d}',
            senha=f'senha {i:02d}',
            cpf=f'cpf {i:02d}',
            data_nascimento=datetime(2025, 1, i).date(),
            status=True,
            data_cadastro=datetime(2025, 1, i).date(),
            rua_usuario=f'rua_usuario {i:02d}',
            bairro_usuario=f'bairro_usuario {i:02d}',
            cidade_usuario=i,
            cep_usuario=f'cep_usuario {i:02d}',
            telefone=f'telefone {i:02d}'
        )
        doadores.append(doador)
    return doadores

@pytest.fixture
def doacao_exemplo():
    from data.model.doacao_model import Doacao
    doacao = Doacao(
        cod_doacao=1,
        cod_doador=1,
        cod_agendamento=None,
        data_hora=datetime(2025, 1, 1, 1, 0, 0),
        quantidade=10,
        status=1
    )
    return doacao

@pytest.fixture
def lista_doacoes_exemplo():
    from data.model.doacao_model import Doacao
    doacoes = []
    for i in range(1, 11):
        doacao = Doacao(
            cod_doacao=i,
            cod_doador=i,
            cod_agendamento=None,
            data_hora=datetime(2025, 1, i, i, 0, 0),
            quantidade=i * 10,
            status=i
        )
        doacoes.append(doacao)
    return doacoes

@pytest.fixture
def exame_exemplo():
    from data.model.exame_model import Exame
    exame = Exame(
        cod_exame=1,
        cod_doacao=1,
        data_exame=datetime(2025, 1, 1).date(),
        tipo_exame="tipo_exame teste",
        resultado="resultado teste",
        arquivo="arquivo teste"
    )
    return exame

@pytest.fixture
def lista_exames_exemplo(): 
    from data.model.exame_model import Exame
    exames = []
    for i in range(1, 11):
        exame = Exame(
            cod_exame=i,
            cod_doacao=i,
            data_exame=datetime(2025, 1, i).date(),
            tipo_exame=f'tipo_exame {i:02d}',
            resultado=f'resultado {i:02d}',
            arquivo=f'arquivo {i:02d}'
        )
        exames.append(exame)
    return exames

@pytest.fixture
def prontuario_exemplo():
    from data.model.prontuario_model import Prontuario
    prontuario = Prontuario(
        cod_prontuario=1,
        cod_doador=1,
        data_criacao=datetime(2025, 1, 1).date(),
        data_atualizacao=datetime(2025, 1, 1).date(),
        diabetes=True,
        hipertensao=True,
        cardiopatia=True,
        cancer=True,
        nenhuma=True,
        outros=True,
        medicamentos="medicamentos teste",
        fumante="fumante teste",
        alcool="alcool teste",
        atividade="atividade teste",
        jejum="jejum teste",
        sono="sono teste",
        bebida="bebida teste",
        sintomas_gripais="sintomas_gripais teste",
        tatuagem="tatuagem teste",
        termos="termos teste",
        alerta="alerta teste"
    )
    return prontuario

@pytest.fixture
def lista_prontuarios_exemplo():
    from data.model.prontuario_model import Prontuario
    prontuarios = []
    for i in range(1, 11):
        prontuario = Prontuario(
            cod_prontuario=i,
            cod_doador=i,
            data_criacao=datetime(2025, 1, i).date(),
            data_atualizacao=datetime(2025, 1, i).date(),
            diabetes=True,
            hipertensao=True,
            cardiopatia=True,
            cancer=True,
            nenhuma=True,
            outros=True,
            medicamentos=f'medicamentos {i:02d}',
            fumante=f'fumante {i:02d}',
            alcool=f'alcool {i:02d}',
            atividade=f'atividade {i:02d}',
            jejum=f'jejum {i:02d}',
            sono=f'sono {i:02d}',
            bebida=f'bebida {i:02d}',
            sintomas_gripais=f'sintomas_gripais {i:02d}',
            tatuagem=f'tatuagem {i:02d}',
            termos=f'termos {i:02d}',
            alerta=f'alerta {i:02d}'
        )
        prontuarios.append(prontuario)
    return prontuarios