from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/contato")
async def get_contato(request: Request):
    response = templates.TemplateResponse("publico/publico_contato.html", {"request": request, "active_page": "contato"})
    return response