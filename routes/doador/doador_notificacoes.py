from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import notificacao_repo
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/notificacao")
@requer_autenticacao(["doador"])
async def get_doador_notificacao(request: Request, usuario_logado: dict = None):
    notificacao = notificacao_repo.obter_todos()
    if notificacao:
        response = templates.TemplateResponse("doador/doador_notificacao.html",
            {"request": request, "active_page": "notificacao", "usuario": usuario_logado, "notificacao": notificacao})
        return response