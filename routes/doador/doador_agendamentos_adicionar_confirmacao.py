from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/agendamento/adicionar/confirmacao")
@requer_autenticacao(["doador"])
async def get_doador_agendamento_adicionar_confirmacao(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("doador/doador_agendamento_adicionar_confirmacao.html", {"request": request, "active_page": "agendamento", "usuario": usuario_logado})
    return response