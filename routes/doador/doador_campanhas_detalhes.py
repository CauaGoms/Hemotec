from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/campanha/detalhes")
async def get_doador_campanha_detalhes(request: Request):
    response = templates.TemplateResponse("doador/doador_campanha_detalhes.html", {"request": request, "active_page": "campanha"})
    return response