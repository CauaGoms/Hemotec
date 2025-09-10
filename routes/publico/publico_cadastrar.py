from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cadastrar")
async def get_cadastro(request: Request):
    response = templates.TemplateResponse("publico/publico_cadastrar_doador.html", {"request": request})
    return response