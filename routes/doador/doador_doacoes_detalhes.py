from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/doacoes/detalhes")
async def get_doador_doacoes_detalhes(request: Request):
    response = templates.TemplateResponse("doador/doador_doacoes_detalhes.html", {"request": request, "active_page": "notificacao"})
    return response