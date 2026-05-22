from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/doador/agendamento/adicionar/confirmacao")
@requer_autenticacao(["doador"])
async def get_doador_agendamento_adicionar_confirmacao(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("doador/doador_agendamento_adicionar_confirmacao.html", {"request": request, "active_page": "agendamento", "usuario": usuario_logado})
    return response