from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/contato")
async def get_contato(request: Request):
    response = templates.TemplateResponse("publico/boas_vindas_contato.html", {"request": request, "active_page": "contato"})
    return response