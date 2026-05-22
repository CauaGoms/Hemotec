from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/adquirir_assinatura")
async def get_adquirir_assinatura(request: Request):
    response = templates.TemplateResponse("publico/publico_adquirir_assinatura.html", {"request": request, "active_page": "home"})
    return response