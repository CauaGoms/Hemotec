from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/usuario/sair")
async def get_usuario_sair(request: Request):
    response = templates.TemplateResponse("usuario/usuario_sair.html", {"request": request, "active_page": "sair"})
    return response
