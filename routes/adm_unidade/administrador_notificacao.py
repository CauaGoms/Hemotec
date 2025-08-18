from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/notificacao")
async def administrador_notificacao(request: Request):
    response = templates.TemplateResponse("adm_unidade/administrador_notificacao.html", {"request": request, "active_page": "perfil"})
    return response