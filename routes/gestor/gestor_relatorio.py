from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/gestor/relatorio")
@requer_autenticacao(["gestor"])
async def get_gestor_relatorio(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse(
        "gestor/gestor_relatorio.html", 
        {
            "request": request, 
            "active_page": "relatorio",
            "usuario": usuario_logado
        }
    )
    return response