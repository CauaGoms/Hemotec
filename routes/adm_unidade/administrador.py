from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador")
async def get_administrador_home(request: Request):
    response = templates.TemplateResponse("adm_unidade/administrador_inicio.html", {"request": request, "active_page": "home"})
    return response