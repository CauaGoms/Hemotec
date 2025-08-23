from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/visualizar_plano")
async def get_visualizar_plano(request: Request):
    response = templates.TemplateResponse("publico/publico_visualizar_plano.html", {"request": request, "active_page": "home"})
    return response