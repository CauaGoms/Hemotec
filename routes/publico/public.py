from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from datetime import date

from data.util.database import get_connection

from data.model.usuario_model import Usuario
from data.model.cidade_model import Cidade

from data.repo import cidade_repo
from data.repo import usuario_repo
from data.repo import unidade_coleta_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_home(request: Request):
    response = templates.TemplateResponse(
        "publico/boas_vindas_inicio.html", {"request": request, "active_page": "inicio"})
    return response

@router.get("/api/unidades")
async def get_api_unidades():
    """
    Esta é uma rota de API. Ela não retorna HTML.
    Ela retorna apenas os dados das unidades de coleta em formato JSON.
    """
    coordenadas = unidade_coleta_repo.obter_coordenada() or []
    return coordenadas

@router.get("/sobre")
async def get_sobre(request: Request):
    response = templates.TemplateResponse("publico/boas_vindas_sobre.html", {"request": request, "active_page": "sobre"})
    return response

@router.get("/campanha")
async def get_campanha(request: Request):
    response = templates.TemplateResponse("publico/boas_vindas_campanha.html", {"request": request, "active_page": "campanha"})
    return response

@router.get("/contato")
async def get_contato(request: Request):
    response = templates.TemplateResponse("publico/boas_vindas_contato.html", {"request": request, "active_page": "contato"})
    return response

@router.get("/login")
async def get_login(request: Request):
    response = templates.TemplateResponse("publico/login.html", {"request": request})
    return response

@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...)
):
    usuario = usuario_repo.obter_por_email(email)
    if usuario and usuario.senha == senha:
        request.session["user_email"] = email
        return RedirectResponse("/doador", status_code=303)
    else:
        raise Exception("Usuário ou senha inválidos.")

@router.get("/recuperar_senha")
async def get_recuperar_senha(request: Request):
    response = templates.TemplateResponse("publico/esqueceu_senha.html", {"request": request})
    return response

@router.get("/cadastro")
async def get_cadastro(request: Request):
    response = templates.TemplateResponse("publico/cadastro.html", {"request": request})
    return response

@router.post("/cadastro")
async def post_cadastro(
    request: Request,
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
    
    email_usuario = email
    # Verifica se já existe usuário com esse e-mail
    if usuario_repo.obter_por_email(email):
        raise Exception("Já existe uma conta cadastrada com esse e-mail.")

    # Busca a cidade pelo nome ou cria uma nova se não existir
    cidade = cidade_repo.obter_por_nome(cidade_usuario)
    if not cidade:
        # Se a cidade não existe, cria uma nova com sigla padrão
        nova_cidade = Cidade(0, cidade_usuario, "SP")  # Usando SP como estado padrão
        cidade_id = cidade_repo.inserir(nova_cidade)
    else:
        cidade_id = cidade.cod_cidade

    status = 1
    data_cadastro = date.today().isoformat()
    usu = Usuario(0, nome, email, senha, cpf, data_nascimento, status, data_cadastro, rua_usuario, bairro_usuario, cidade_id, cep_usuario, telefone)
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario_id = usuario_repo.inserir(usu, cursor)
        conn.commit()
    if usuario_id is None:
        raise Exception("Erro ao cadastrar usuário.")
    else:
        return RedirectResponse("/doador/novo_doador", status_code=303)