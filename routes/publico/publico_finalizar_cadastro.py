from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/finalizar_cadastro")
async def get_finalizar_cadastro(request: Request):
    response = templates.TemplateResponse("publico/publico_finalizar_cadastro.html", {"request": request, "active_page": "home"})
    return response