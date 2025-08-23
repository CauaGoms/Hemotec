from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/confirmar_cadastro")
async def get_confirmar_cadastro(request: Request):
    response = templates.TemplateResponse("publico/publico_confirmar_cadastro.html", {"request": request, "active_page": "home"})
    return response