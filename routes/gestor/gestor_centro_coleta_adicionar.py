from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/gestor/centrocoleta/adicionar")
async def get_doador_home(request: Request):
    response = templates.TemplateResponse("gestor/gestor_centro_coleta_adicionar.html", {"request": request, "active_page": "relatorio"})
    return response