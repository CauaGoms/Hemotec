from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from util.auth_decorator import esta_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cadastrar")
async def get_cadastro(request: Request):
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("publico/publico_cadastrar_doador.html", {"request": request})