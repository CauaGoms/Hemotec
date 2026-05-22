from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from util.jinja_custom import CorrecaoJinjaTemplates

from data.repo import usuario_repo

router = APIRouter()
templates = CorrecaoJinjaTemplates(directory="templates")

@router.get("/login")
async def get_login(request: Request):
    response = templates.TemplateResponse("publico/publico_login.html", {"request": request})
    return response