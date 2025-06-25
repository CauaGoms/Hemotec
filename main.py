from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from datetime import date

from data.util import get_connection

from data.model.usuario_model import Usuario
from data.model.prontuario_model import Prontuario
from data.model.doador_model import Doador

from data.repo import cidade_repo
from data.repo import campanha_repo
from data.repo import usuario_repo
from data.repo import gestor_repo
from data.repo import instituicao_repo
from data.repo import assinatura_repo
from data.repo import plano_repo
from data.repo import licenca_repo
from data.repo import adm_unidade_repo
from data.repo import adm_campanha_repo
from data.repo import unidade_coleta_repo
from data.repo import estoque_repo
from data.repo import notificacao_repo
from data.repo import colaborador_repo
from data.repo import agendamento_repo
from data.repo import doador_repo
from data.repo import doacao_repo
from data.repo import exame_repo
from data.repo import prontuario_repo
from data.repo import prontuario_repo

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

cidade_repo.criar_tabela()
campanha_repo.criar_tabela()
usuario_repo.criar_tabela()
gestor_repo.criar_tabela()
instituicao_repo.criar_tabela()
assinatura_repo.criar_tabela()
plano_repo.criar_tabela()
licenca_repo.criar_tabela()
adm_unidade_repo.criar_tabela()
adm_campanha_repo.criar_tabela()
unidade_coleta_repo.criar_tabela()
estoque_repo.criar_tabela()
notificacao_repo.criar_tabela()
colaborador_repo.criar_tabela()
agendamento_repo.criar_tabela()
doador_repo.criar_tabela()
doacao_repo.criar_tabela()
exame_repo.criar_tabela()
prontuario_repo.criar_tabela()
prontuario_repo.criar_tabela()


email_usuario = ""
@app.get("/")
async def get_root():
    coordenada = unidade_coleta_repo.obter_coordenada() or []
    response = templates.TemplateResponse("boas_vindas_inicio.html", {"request": {}, "active_page": "inicio", "coordenada": coordenada})
    return response

@app.get("/sobre")
async def get_root():
    response = templates.TemplateResponse("boas_vindas_sobre.html", {"request": {}, "active_page": "sobre"})
    return response

@app.get("/campanha")
async def get_root():
    response = templates.TemplateResponse("boas_vindas_campanha.html", {"request": {}, "active_page": "campanha"})
    return response

@app.get("/contato")
async def get_root():
    response = templates.TemplateResponse("boas_vindas_contato.html", {"request": {}, "active_page": "contato"})
    return response

@app.get("/login")
async def get_root():
    response = templates.TemplateResponse("login.html", {"request": {}})
    return response

@app.post("/login")
async def post_login(
    email: str = Form(...),
    senha: str = Form(...)
):
    usuario = usuario_repo.obter_por_email(email)
    if usuario and usuario.senha == senha:
        return RedirectResponse("/doador", status_code=303)
    else:
        raise Exception("Usuário ou senha inválidos.")

@app.get("/recuperar_senha")
async def get_root():
    response = templates.TemplateResponse("esqueceu_senha.html", {"request": {}})
    return response

@app.get("/cadastro")
async def get_root():
    response = templates.TemplateResponse("cadastro.html", {"request": {}})
    return response

@app.post("/cadastro")
async def post_cadastro(
    nome: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cep_usuario: str = Form(...),
    rua_usuario: str = Form(...),
    bairro_usuario: str = Form(...),
    cidade_usuario: str = Form(...),
    senha: str = Form(...)
):
    
    email_usuario= email
    # Verifica se já existe usuário com esse e-mail
    if usuario_repo.obter_por_email(email):
        raise Exception("Já existe uma conta cadastrada com esse e-mail.")

    status = 1
    data_cadastro = date.today().isoformat()
    usu = Usuario(0, nome, email, senha, cpf, data_nascimento, status, data_cadastro, rua_usuario, bairro_usuario, cidade_usuario, cep_usuario, telefone)
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario_id = usuario_repo.inserir(usu, cursor)
        conn.commit()
    if usuario_id is None:
        raise Exception("Erro ao cadastrar usuário.")
    else:
        return RedirectResponse("/doador/novo_doador", status_code=303)

@app.get("/doador")
async def get_root():
    response = templates.TemplateResponse("doador_inicio.html", {"request": {}, "active_page": "home"})
    return response

@app.get("/doador/campanha")
async def get_root():
    response = templates.TemplateResponse("doador_campanha.html", {"request": {}, "active_page": "campanha"})
    return response

@app.get("/doador/agendamento")
async def get_root():
    response = templates.TemplateResponse("doador_agendamento.html", {"request": {}, "active_page": "agendamento"})
    return response

@app.get("/doador/notificacao")
async def get_root():
    response = templates.TemplateResponse("doador_notificacao.html", {"request": {}, "active_page": "notificacao"})
    return response

@app.get("/doador/meu_perfil")
async def get_root():
    response = templates.TemplateResponse("doador_meu_perfil.html", {"request": {}, "active_page": "perfil"})
    return response

@app.get("/doador/configuracoes")
async def get_root():
    response = templates.TemplateResponse("doador_configuracoes.html", {"request": {}, "active_page": "perfil"})
    return response

@app.get("/doador/novo_doador")
async def get_root():
    response = templates.TemplateResponse("primeira_doacao.html", {"request": {}})
    return response

@app.post("/doador/novo_doador")
async def post_novo_doador(
    altura: float = Form(...),
    peso: int = Form(...),
    tipo_sanguineo: str = Form(...),
    profissao: str = Form(...),
    contato_emergencia: str = Form(...),
    telefone_emergencia: str = Form(...),
    diabetes: bool = Form(False),
    hipertensao: bool = Form(False),
    cardiopatia: bool = Form(False),
    cancer: bool = Form(False),
    nenhuma: bool = Form(False),
    outros: bool = Form(False),
    medicamentos: str = Form("Nenhum"),
    fumante: str = Form("Não"),
    alcool: str = Form("Não"),
    atividade_fisica: str = Form("Não"),
    jejum: str = Form(False),
    sono: str = Form(False),
    bebida: str = Form(False),
    sintomas_gripais: str = Form(False),
    tatuagem: str = Form(False),
    termos: str = Form(False),
    alerta: str = Form(False)
):
    # 1. Obtenha o identificador do usuário logado
    email_usuario = email_usuario  

    # 2. Busque o usuário no banco
    usuario = usuario_repo.obter_por_email(email_usuario)
    if not usuario:
        raise Exception("Usuário não encontrado.")

    data_atualizacao = date.today().isoformat()
    prontuario = Prontuario(
        0, 0, data_atualizacao, data_atualizacao, diabetes, hipertensao, cardiopatia, cancer, nenhuma, outros,
        medicamentos, fumante, alcool, atividade_fisica, jejum, sono, bebida, sintomas_gripais, tatuagem, termos, alerta
    )

    elegivel = True  # Defina a elegibilidade como True por padrão

    # extraindo o fator Rh do tipo sanguíneo
    fator_rh = ""
    if tipo_sanguineo.endswith("+"):
        fator_rh = "+"
    elif tipo_sanguineo.endswith("-"):
        fator_rh = "-"
    # 3. Crie o doador usando os dados do usuário buscado
    doador = Doador(
        0, 0, 0, tipo_sanguineo, fator_rh, elegivel, altura, peso, profissao, contato_emergencia, telefone_emergencia
    )

    with get_connection() as conn:
        cursor = conn.cursor()
        prontuario_id = usuario_repo.inserir(prontuario, cursor)
        doador_id = doador_repo.inserir(doador, cursor)
        conn.commit()
    if prontuario_id or doador_id is None:
        raise Exception("Erro ao cadastrar prontuario ou doador.")
    else:
        return RedirectResponse("/doador", status_code=303)

# @app.route('/doador/novo_doador')
# def primeira_doacao():
#     cod_doador = ... # recupere o código do doador logado
#     idade_apta = verificar_idade_doador(cod_doador)
#     return templates.TemplateResponse("primeira_doacao.html", {"request": {}, "idade_apta": idade_apta})



   






# @app.get("/admin/produtos")
# async def get_produtos():
#     produtos = produto_repo.obter_todos()
#     response = templates.TemplateResponse("produtos.html", {"request": {}, "produtos": produtos})
#     return response

# @app.get("/produtos/{id}")
# async def get_produto_por_id(id: int):
#     produto = produto_repo.obter_por_id(id)
#     response = templates.TemplateResponse("produto.html", {"request": {}, "produto": produto})
#     return response

# @app.get("/admin/produtos/cadastrar")
# async def get_produto_cadastrar():
#     response = templates.TemplateResponse("cadastrar_produto.html", {"request": {}})
#     return response

# @app.post("/admin/produtos/cadastrar")
# async def post_produto_cadastrar(
#     nome: str = Form(...),
#     descricao: str = Form(...),
#     preco: float = Form(...),
#     quantidade: int = Form(...)
# ):
#     produto = Produto(0, nome, descricao, preco, quantidade)
#     id_produto = produto_repo.inserir(produto)
#     if id_produto == None:
#         raise Exception("Erro ao inserir produto.")
#     else:
#         return RedirectResponse("/produtos", status_code=303)
    

# @app.get("/admin/clientes")
# async def get_clientes():
#     clientes = cliente_repo.obter_todos()
#     response = templates.TemplateResponse("clientes.html", {"request": {}, "clientes": clientes})
#     return response


# @app.get("/admin/formas_pagamento")
# async def get_formas_pagamento():
#     formas_pagamento = forma_pagamento_repo.obter_todas()
#     response = templates.TemplateResponse("formas_pagamento.html", {"request": {}, "formas_pagamento": formas_pagamento})
#     return response


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)