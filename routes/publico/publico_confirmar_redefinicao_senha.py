from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/confirmar_redefinicao_senha")
async def get_confirmar_redefinicao_senha(request: Request):
    response = templates.TemplateResponse("publico/publico_confirmar_redefinicao_senha.html", {"request": request})
    return response