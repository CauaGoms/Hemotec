from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador")
async def get_colaborador_home(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_inicio.html", {"request": request, "active_page": "home"})
    return response
