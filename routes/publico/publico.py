from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_doador_home(request: Request):
    # Buscar campanhas recentes e ativas (limitando a 3 para exibição na página inicial)
    campanhas = campanha_repo.obter_todos()
    
    # Filtrar campanhas ativas (status 1) e ordenar por data de início
    campanhas_ativas = [c for c in campanhas if c.status == '1']
    campanhas_ativas.sort(key=lambda x: x.data_inicio, reverse=True)
    campanhas_recentes = campanhas_ativas[:3] if campanhas_ativas else []
    
    response = templates.TemplateResponse(
        "publico/publico_inicio.html", 
        {
            "request": request, 
            "active_page": "home",
            "campanhas": campanhas_recentes
        }
    )
    return response