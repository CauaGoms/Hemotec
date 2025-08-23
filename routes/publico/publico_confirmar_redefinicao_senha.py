from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/confirmar_redefinicao_senha")
async def get_confirmar_redefinicao_senha(request: Request):
    response = templates.TemplateResponse("publico/publico_confirmar_redefinicao_senha.html", {"request": request})
    return response