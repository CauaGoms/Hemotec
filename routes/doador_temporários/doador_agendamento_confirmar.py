from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/agendamento/confirmar")
async def get_doador_confirmar(request: Request):
    response = templates.TemplateResponse("doador/doador_confirmar.html", {"request": request, "active_page": "agendamento"})
    return response