from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/colaborador/doacao/excluir")
async def get_colaborador_doacao_excluir(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_doacao_excluir.html", {"request": request, "active_page": "doacoes"})
    return response
