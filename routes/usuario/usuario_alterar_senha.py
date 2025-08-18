from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/usuario/alterar_senha")
async def get_usuario_alterar_senha(request: Request):
    response = templates.TemplateResponse("usuario/usuario_alterar_senha.html", {"request": request, "active_page": "alterar_senha"})
    return response
