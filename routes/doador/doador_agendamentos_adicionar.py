from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates
from util.auth_decorator import requer_autenticacao
from data.repo import unidade_coleta_repo

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/doador/agendamento/adicionar")
@requer_autenticacao(["doador"])
async def get_doador_agendamento_adicionar(request: Request, usuario_logado: dict = None):
    # Buscar todas as unidades de coleta do banco de dados
    unidades = unidade_coleta_repo.obter_todos() or []
    
    response = templates.TemplateResponse("doador/doador_agendamento_adicionar.html", {
        "request": request, 
        "active_page": "agendamento", 
        "usuario": usuario_logado,
        "unidades": unidades
    })
    return response