from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/configuracoes")
@requer_autenticacao(["doador"])
async def get_doador_configuracoes(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("doador/doador_configuracoes.html", {"request": request, "active_page": "perfil", "usuario": usuario_logado})
    return response