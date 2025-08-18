from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/agendamento/adicionar")
async def get_colaborador_agendamento_adicionar(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_agendamento_adicionar.html", {"request": request, "active_page": "adicionar"})
    return response
