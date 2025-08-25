from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/telas_teste/doador/reagendamento")
async def get_doador_reagendamento(request: Request):
    response = templates.TemplateResponse("telas_teste/doador_reagendamento.html", {"request": request, "active_page": "agendamento"})
    return response