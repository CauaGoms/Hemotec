from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/agendamento/excluir")
async def get_colaborador_agendamento_excluir(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_agendamento_excluir.html", {"request": request, "active_page": "agendamento"})
    return response
