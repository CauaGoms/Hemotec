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
    hoje = datetime.now().date()
    
    def get_status_order(campanha):
        if campanha.data_inicio > hoje:
            return (1, campanha.data_inicio) 
        elif campanha.data_fim >= hoje:
            return (0, campanha.data_inicio)
        else:
            return (2, -campanha.data_fim.toordinal())
    campanhas_ordenadas = sorted(campanhas, key=get_status_order)
    
    response = templates.TemplateResponse("doador/doador_campanha.html", {
        "request": request, 
        "active_page": "campanha", 
        "usuario": usuario_logado, 
        "campanhas": campanhas_ordenadas, 
        "now": datetime.now
    })
    return response