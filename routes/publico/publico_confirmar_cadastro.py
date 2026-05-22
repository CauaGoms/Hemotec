from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/confirmar_cadastro")
async def get_confirmar_cadastro(request: Request):
    response = templates.TemplateResponse("publico/publico_confirmar_cadastro.html", {"request": request, "active_page": "home"})
    return response