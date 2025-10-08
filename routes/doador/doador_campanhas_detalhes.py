from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# @router.get("/doador/campanha/detalhes")
# async def get_doador_campanha_detalhes(request: Request):
#     response = templates.TemplateResponse("doador/doador_campanha_detalhes.html", {"request": request, "active_page": "campanha"})
#     return response

@router.get("/campanha/detalhes/{id}")
@requer_autenticacao(["doador"])
async def get_doador_campanha_detalhes(request: Request, id: int, usuario_logado: dict = None):
    campanha = campanha_repo.obter_por_id(id)
    if campanha:
        response = templates.TemplateResponse("doador/doador_campanha_detalhes.html",
            {"request": request, "active_page": "campanha", "usuario": usuario_logado, "campanha": campanha})
        return response