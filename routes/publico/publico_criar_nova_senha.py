from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/criar_nova_senha")
async def get_criar_nova_senha(request: Request):
    response = templates.TemplateResponse("publico/publico_criar_nova_senha.html", {"request": request})
    return response