from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador")
@requer_autenticacao(["administrador"])
async def get_administrador_home(request: Request, usuario_logado: dict = None):
    from data.repo import campanha_repo, notificacao_repo
    
    # Buscar campanhas e notificações do banco
    campanhas_ativas = campanha_repo.obter_todos()
    notificacoes_recentes = notificacao_repo.obter_todos()
    
    response = templates.TemplateResponse(
        "adm_unidade/administrador_inicio.html", 
        {
            "request": request, 
            "usuario": usuario_logado,
            "active_page": "home",
            "campanhas_ativas": campanhas_ativas,
            "notificacoes_recentes": notificacoes_recentes
        }
    )
    return response