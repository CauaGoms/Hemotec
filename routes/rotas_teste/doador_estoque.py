from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/telas_teste/doador/estoque")
async def doador_estoque(request: Request):
    response = templates.TemplateResponse("telas_teste/doador_estoque.html", {"request": request, "active_page": "estoque"})
    return response