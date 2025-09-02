from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import notificacao_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# @router.get("/doador/notificacao")
# async def get_doador_notificacao(request: Request):
#     response = templates.TemplateResponse("doador/doador_notificacao.html", {"request": request, "active_page": "notificacao"})
#     return response

@router.get("/doador/notificacao")
async def get_doador_notificacao(request: Request):
    notificacao = notificacao_repo.obter_todos()
    if notificacao:
        response = templates.TemplateResponse("doador/doador_notificacao.html",
            {"request": request, "active_page": "notificacao", "notificacao": notificacao})
        return response