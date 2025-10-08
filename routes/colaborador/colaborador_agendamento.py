from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/agendamento")
@requer_autenticacao(["colaborador"])
async def get_colaborador_agendamento(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse(
        "colaborador/colaborador_agendamento.html", 
        {
            "request": request, 
            "active_page": "agendamento",
            "usuario": usuario_logado
        }
    )
    return response
