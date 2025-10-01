from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/doacao/excluir")
async def get_colaborador_doacao_excluir(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_doacao_excluir.html", {"request": request, "active_page": "doacoes"})
    return response
