from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/notificacao")
async def get_colaborador_notificacao(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_notificacao.html", {"request": request, "active_page": "notificacao"})
    return response
