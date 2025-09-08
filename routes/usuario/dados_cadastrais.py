from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dados_cadastrais")
async def get_doador_dados_cadastrais(request: Request):
    response = templates.TemplateResponse("doador/doador_dados_cadastrais.html", {"request": request, "active_page": "perfil"})
    return response