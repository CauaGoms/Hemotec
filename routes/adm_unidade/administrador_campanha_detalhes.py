from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/campanha/detalhes")
async def administrador_campanha_detalhes(request: Request):
    response = templates.TemplateResponse("adm_unidade/administrador_campanha_detalhes.html", {"request": request, "active_page": "perfil"})
    return response