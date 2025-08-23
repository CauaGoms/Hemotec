from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from data.repo import usuario_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def get_login(request: Request):
    response = templates.TemplateResponse("publico/publico_login.html", {"request": request})
    return response

@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...)
):
    usuario = usuario_repo.obter_por_email(email)
    if usuario and usuario.senha == senha:
        request.session["user_email"] = email
        return RedirectResponse("/doador", status_code=303)
    else:
        raise Exception("Usuário ou senha inválidos.")