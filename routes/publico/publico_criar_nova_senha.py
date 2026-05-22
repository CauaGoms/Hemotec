from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/criar_nova_senha")
async def get_criar_nova_senha(request: Request):
    response = templates.TemplateResponse("publico/publico_criar_nova_senha.html", {"request": request})
    return response

@router.post("/criar_nova_senha")
async def get_criar_nova_senha(request: Request):
    response = templates.TemplateResponse("publico/publico_criar_nova_senha.html", {"request": request})
    return response