from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/validar_telefone")
async def get_validar_telefone(request: Request):
    response = templates.TemplateResponse("publico/publico_validar_telefone.html", {"request": request, "active_page": "home"})
    return response

@router.post("/validar_telefone")
async def get_validar_telefone(request: Request):
    response = templates.TemplateResponse("publico/publico_validar_telefone.html", {"request": request, "active_page": "home"})
    return response