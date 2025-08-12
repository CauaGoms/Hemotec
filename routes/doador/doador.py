from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from datetime import date

from data.util.database import get_connection

from data.model.usuario_model import Usuario
from data.model.cidade_model import Cidade
from data.model.prontuario_model import Prontuario

router = APIRouter()
templates = Jinja2Templates(directory="templates")

from data.model.doador_model import Doador

from data.repo import cidade_repo
from data.repo import usuario_repo
from data.repo import unidade_coleta_repo
from data.repo import prontuario_repo
from data.repo import doador_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador")
async def get_doador_home(request: Request):
    response = templates.TemplateResponse("doador/doador_inicio.html", {"request": request, "active_page": "home"})
    return response




