from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/campanha")
async def get_campanha(request: Request):
    campanhas = campanha_repo.obter_todos()
    response = templates.TemplateResponse("publico/publico_campanha.html", {"request": request, "active_page": "campanha", "campanhas": campanhas})
    return response