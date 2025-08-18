from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/campanha")
async def get_colaborador_campanha(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_campanha.html", {"request": request, "active_page": "campanha"})
    return response
