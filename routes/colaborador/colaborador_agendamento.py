from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/agendamento")
async def get_colaborador_agendamento(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_agendamento.html", {"request": request, "active_page": "agendamento"})
    return response
