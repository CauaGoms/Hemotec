from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo
from util.auth_decorator import requer_autenticacao
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/campanha/detalhes/{cod_campanha}")
@requer_autenticacao(["doador"])
async def get_doador_campanha_detalhes(request: Request, cod_campanha: int, usuario_logado: dict = None):
    campanha = campanha_repo.obter_por_id(cod_campanha)
    if campanha:
        response = templates.TemplateResponse(
            "doador/doador_campanha_detalhes.html",
            {"request": request, "active_page": "campanha", "usuario": usuario_logado, "campanha": campanha, "now": datetime.now}
        )
        return response