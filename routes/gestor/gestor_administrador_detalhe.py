from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/gestor/administrador/detalhe")
async def get_doador_home(request: Request):
    response = templates.TemplateResponse("gestor/gestor_administrador_detalhe.html", {"request": request, "active_page": "relatorio"})
    return response