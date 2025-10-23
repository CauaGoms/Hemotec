from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from util.auth_decorator import esta_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cadastrar")
async def get_cadastro(request: Request):
    # Verificar se o usuário está logado e seu tipo de acesso
    if esta_logado(request):
        # Permitir que colaboradores e gestores acessem a página de cadastro
        tipo_acesso = request.session.get("tipo_acesso", "").lower()
        if tipo_acesso not in ["colaborador", "gestor", "administrador"]:
            # Apenas doadores e outros tipos são redirecionados
            return RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("publico/publico_cadastrar_doador.html", {"request": request})