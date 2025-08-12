from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/carteira")
async def get_doador_carteira(request: Request):
    response = templates.TemplateResponse("doador/doador_carteira.html", {"request": request, "active_page": "carteira"})
    return response