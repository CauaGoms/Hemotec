from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/doacao/detalhe")
async def get_colaborador_doacao_detalhe(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_doacao_detalhe.html", {"request": request, "active_page": "doacao"})
    return response
