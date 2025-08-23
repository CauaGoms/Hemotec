from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cadastrar_possivel_gestor")
async def get_cadastrar_possivel_gestor(request: Request):
    response = templates.TemplateResponse("publico/publico_cadastrar_possivel_gestor.html", {"request": request, "active_page": "home"})
    return response