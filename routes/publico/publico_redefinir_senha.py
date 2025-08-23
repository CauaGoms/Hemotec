from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/redefinir_senha")
async def get_redefinir_senha(request: Request):
    response = templates.TemplateResponse("publico/publico_redefinir_senha.html", {"request": request})
    return response