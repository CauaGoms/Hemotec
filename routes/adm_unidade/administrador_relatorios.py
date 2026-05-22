from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/administrador/relatorio")
@requer_autenticacao(["administrador"])
async def administrador_relatorios(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse(
        "adm_unidade/administrador_relatorios.html", 
        {
            "request": request, 
            "active_page": "relatorio",
            "usuario": usuario_logado
        }
    )
    return response