from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/relatorio")
async def administrador_relatorios(request: Request):
    response = templates.TemplateResponse("adm_unidade/administrador_relatorios.html", {"request": request, "active_page": "perfil"})
    return response