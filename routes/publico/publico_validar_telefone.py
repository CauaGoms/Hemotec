from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/validar_telefone")
async def get_validar_telefone(request: Request):
    response = templates.TemplateResponse("publico/publico_validar_telefone.html", {"request": request, "active_page": "home"})
    return response

@router.post("/validar_telefone")
async def get_validar_telefone(request: Request):
    response = templates.TemplateResponse("publico/publico_validar_telefone.html", {"request": request, "active_page": "home"})
    return response