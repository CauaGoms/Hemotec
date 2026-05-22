from fastapi import APIRouter, Request
from util.jinja_custom import CorrecaoJinjaTemplates

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/sobre")
async def get_sobre(request: Request):
    response = templates.TemplateResponse("publico/publico_sobre.html", {"request": request, "active_page": "sobre"})
    return response