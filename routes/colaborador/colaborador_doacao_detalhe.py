from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/colaborador/doacao/detalhe")
async def get_colaborador_doacao_detalhe(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_doacao_detalhe.html", {"request": request, "active_page": "doacoes"})
    return response
