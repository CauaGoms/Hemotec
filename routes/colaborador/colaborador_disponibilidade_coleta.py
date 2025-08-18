from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/disponibilidade_coleta")
async def get_colaborador_disponibilidade_coleta(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_disponibilidade_coleta.html", {"request": request, "active_page": "disponibilidade"})
    return response
