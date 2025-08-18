from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/usuario/sair")
async def get_usuario_sair(request: Request):
    response = templates.TemplateResponse("usuario/usuario_sair.html", {"request": request, "active_page": "sair"})
    return response
