from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/campanha/adicionar")
async def get_colaborador_campanha_adicionar(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_campanha_adicionar.html", {"request": request, "active_page": "campanha"})
    return response
