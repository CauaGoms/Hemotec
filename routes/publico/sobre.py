from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/sobre")
async def get_sobre(request: Request):
    response = templates.TemplateResponse("publico/boas_vindas_sobre.html", {"request": request, "active_page": "sobre"})
    return response