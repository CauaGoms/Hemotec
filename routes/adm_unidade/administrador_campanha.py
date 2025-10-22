from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo
from datetime import date

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/campanha")
async def administrador_campanha(request: Request):
    # Buscar todas as campanhas do banco de dados
    campanhas = campanha_repo.obter_todos()
    
    response = templates.TemplateResponse("adm_unidade/administrador_campanha.html", {
        "request": request,
        "active_page": "campanha",
        "campanhas": campanhas,
        "hoje": date.today()
    })
    return response