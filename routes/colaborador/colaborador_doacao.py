from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/doacao")
async def get_colaborador_doacao(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_doacao.html", {"request": request, "active_page": "doacoes"})
    return response
