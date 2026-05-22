from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates
from data.repo import colaborador_repo
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/administrador/colaboradores")
@requer_autenticacao(["administrador"])
async def administrador_colaboradores(request: Request, usuario_logado: dict = None):
    # Buscar todos os colaboradores do banco de dados
    colaboradores = colaborador_repo.obter_todos()
    
    response = templates.TemplateResponse("adm_unidade/administrador_colaboradores.html", {
        "request": request,
        "active_page": "colaborador",
        "colaboradores": colaboradores,
        "usuario": usuario_logado
    })
    return response