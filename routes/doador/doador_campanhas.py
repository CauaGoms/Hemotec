from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo
from util.auth_decorator import requer_autenticacao
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/campanha")
@requer_autenticacao(["doador"])
async def get_doador_campanha(request: Request, usuario_logado: dict = None):
    campanhas = campanha_repo.obter_todos()
    response = templates.TemplateResponse("doador/doador_campanha.html", {"request": request, "active_page": "campanha", "usuario": usuario_logado, "campanhas": campanhas, "now": datetime.now})
    return response