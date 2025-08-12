from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/meu_perfil")
async def get_doador_perfil(request: Request):
    response = templates.TemplateResponse("doador/doador_meu_perfil.html", {"request": request, "active_page": "perfil"})
    return response