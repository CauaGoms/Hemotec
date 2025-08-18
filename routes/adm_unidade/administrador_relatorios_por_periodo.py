from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/relatorios/periodo")
async def get_administrador_relatorio_por_periodo(request: Request):
    response = templates.TemplateResponse("adm_unidade/administrador_relatorios_por_periodo.html", {"request": request, "active_page": "home"})
    return response