from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/campanha")
async def get_campanha(request: Request):
    response = templates.TemplateResponse("publico/boas_vindas_campanha.html", {"request": request, "active_page": "campanha"})
    return response