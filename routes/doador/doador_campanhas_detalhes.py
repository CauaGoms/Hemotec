from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# @router.get("/doador/campanha/detalhes")
# async def get_doador_campanha_detalhes(request: Request):
#     response = templates.TemplateResponse("doador/doador_campanha_detalhes.html", {"request": request, "active_page": "campanha"})
#     return response

@router.get("/campanha/detalhes/{id}")
async def get_doador_campanha_detalhes(request: Request, id: int):
    campanha = campanha_repo.obter_por_id(id)
    if campanha:
        response = templates.TemplateResponse("doador/doador_campanha_detalhes.html",
            {"request": request, "active_page": "campanha", "campanha": campanha})
        return response