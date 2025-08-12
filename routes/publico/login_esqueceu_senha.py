from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login/recuperar_senha")
async def get_recuperar_senha(request: Request):
    response = templates.TemplateResponse("publico/esqueceu_senha.html", {"request": request})
    return response