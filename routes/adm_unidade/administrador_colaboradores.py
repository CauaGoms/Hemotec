from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/colaboradores")
async def administrador_colaboradores(request: Request):
    response = templates.TemplateResponse("adm_unidade/administrador_colaboradores.html", {"request": request, "active_page": "perfil"})
    return response