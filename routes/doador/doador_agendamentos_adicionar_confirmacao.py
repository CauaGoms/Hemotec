from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/agendamento/adicionar/confirmacao")
async def get_doador_agendamento_adicionar_confirmacao(request: Request):
    response = templates.TemplateResponse("doador/doador_agendamento_adicionar_confirmacao.html", {"request": request, "active_page": "agendamento"})
    return response