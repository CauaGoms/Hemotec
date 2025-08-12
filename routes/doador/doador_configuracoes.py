from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/configuracoes")
async def get_doador_configuracoes(request: Request):
    response = templates.TemplateResponse("doador/doador_configuracoes.html", {"request": request, "active_page": "perfil"})
    return response