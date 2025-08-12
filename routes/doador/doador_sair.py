from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/sair")
async def doador_sair(request: Request):
    response = templates.TemplateResponse("doador/doador_sair.html", {"request": request, "active_page": "perfil"})
    return response