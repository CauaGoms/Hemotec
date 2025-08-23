from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/doacoes")
async def get_doador_doacoes(request: Request):
    response = templates.TemplateResponse("doador/doador_doacoes.html", {"request": request, "active_page": "notificacao"})
    return response