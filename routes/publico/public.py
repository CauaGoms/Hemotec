from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from data.repo import unidade_coleta_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_home(request: Request):
    response = templates.TemplateResponse(
        "publico/boas_vindas_inicio.html", {"request": request, "active_page": "inicio"})
    return response

@router.get("/api/unidades")
async def get_api_unidades():
    """
    Esta é uma rota de API. Ela não retorna HTML.
    Ela retorna apenas os dados das unidades de coleta em formato JSON.
    """
    coordenadas = unidade_coleta_repo.obter_coordenada() or []
    return coordenadas