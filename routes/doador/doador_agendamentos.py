from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/agendamento")
async def get_doador_agendamento(request: Request):
    response = templates.TemplateResponse("doador/doador_agendamento.html", {"request": request, "active_page": "agendamento"})
    return response