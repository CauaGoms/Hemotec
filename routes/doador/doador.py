from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador")
async def get_doador_home(request: Request):
    response = templates.TemplateResponse("doador/doador_inicio.html", {"request": request, "active_page": "home"})
    return response




