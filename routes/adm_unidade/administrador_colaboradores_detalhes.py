from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/colaboradores/detalhes")
async def administrador_colaboradores_detalhes(request: Request):
    response = templates.TemplateResponse("adm_unidade/administrador_colaboradores_detalhes.html", {"request": request, "active_page": "perfil"})
    return response