from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/adquirir_assinatura")
async def get_adquirir_assinatura(request: Request):
    response = templates.TemplateResponse("publico/publico_adquirir_assinatura.html", {"request": request, "active_page": "home"})
    return response