from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import usuario_repo, cidade_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/meu_perfil")
@requer_autenticacao()
async def administrador_meu_perfil(request: Request, usuario_logado: dict = None):
    # Obter informações do usuário
    usuario = usuario_repo.obter_por_id(usuario_logado['cod_usuario'])
    
    # Obter informações da cidade
    cidade = None
    if usuario and usuario.cidade_usuario:
        cidade = cidade_repo.obter_por_id(usuario.cidade_usuario)
    
    response = templates.TemplateResponse(
        "adm_unidade/administrador_meu_perfil.html",
        {
            "request": request,
            "active_page": "perfil",
            "usuario": usuario,
            "cidade": cidade
        }
    )
    return response
