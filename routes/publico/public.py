from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from datetime import date
from typing import Dict, Any


from data.util.database import get_connection

from data.model.usuario_model import Usuario
from data.model.cidade_model import Cidade

from data.repo import cidade_repo
from data.repo import usuario_repo
from data.repo import unidade_coleta_repo
from data.repo import estoque_repo

def calcular_nivel_estoque(quantidade: int) -> Dict[str, Any]:
    maximo_ideal = 10000.0
    porcentagem = min((quantidade / maximo_ideal) * 100, 100)
    if quantidade <= 2000:
        return {"status": "Crítico", "classe": "bg-danger", "porcentagem": porcentagem}
    elif quantidade <= 5000:
        return {"status": "Baixo", "classe": "bg-warning", "porcentagem": porcentagem}
    else:
        return {"status": "Adequado", "classe": "bg-success", "porcentagem": porcentagem}


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

@router.get("/api/estoque/{cod_unidade}")
async def get_api_estoque_unidade(cod_unidade: int):
    """
    API para buscar estoque de uma unidade específica
    """
    try:
        # Busca o estoque da unidade no banco de dados
        estoque_lista = estoque_repo.obter_por_unidade(cod_unidade)
        
        if not estoque_lista:
            return {
                "cod_unidade": cod_unidade,
                "estoque": {},
                "success": True,
                "message": "Nenhum estoque encontrado para esta unidade"
            }
        
        # Organiza os dados por tipo sanguíneo
        estoque_organizado = {}
        for item in estoque_lista:
            tipo_completo = f"{item.tipo_sanguineo}{item.fator_rh}"
            nivel_info = calcular_nivel_estoque(item.quantidade)
            
            estoque_organizado[tipo_completo] = {
                "quantidade": item.quantidade,
                "status": nivel_info["status"],
                "classe": nivel_info["classe"],
                "porcentagem": nivel_info["porcentagem"],
                "data_atualizacao": item.data_atualizacao.isoformat() if item.data_atualizacao else None
            }
        
        return {
            "cod_unidade": cod_unidade,
            "estoque": estoque_organizado,
            "success": True
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

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