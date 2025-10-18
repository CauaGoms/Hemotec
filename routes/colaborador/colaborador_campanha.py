from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo
from datetime import date

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/campanha")
async def get_colaborador_campanha(request: Request):
    # Buscar todas as campanhas do banco de dados
    campanhas = campanha_repo.obter_todos()
    
    response = templates.TemplateResponse("colaborador/colaborador_campanha.html", {
        "request": request, 
        "active_page": "campanha",
        "campanhas": campanhas,
        "hoje": date.today()
    })
    return response
