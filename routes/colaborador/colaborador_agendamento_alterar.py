from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/agendamento/alterar")
async def get_colaborador_agendamento_alterar(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_agendamento_alterar.html", {"request": request, "active_page": "agendamento"})
    return response
