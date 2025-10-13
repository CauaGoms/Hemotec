from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import doador_repo, notificacao_repo
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador")
@requer_autenticacao(["doador"])
async def get_doador_home(request: Request, usuario_logado: dict = None):
    # Buscar as 3 notificações mais recentes do usuário logado (independentemente do status)
    cod_usuario = usuario_logado["cod_usuario"]
    notificacoes_recentes = notificacao_repo.obter_ultimas_recentes(cod_usuario, 3)
    total_nao_lidas = notificacao_repo.contar_nao_lidas(cod_usuario)
    
    response = templates.TemplateResponse("doador/doador_inicio.html", {
        "request": request, 
        "active_page": "home", 
        "usuario": usuario_logado,
        "notificacoes_recentes": notificacoes_recentes,
        "total_nao_lidas": total_nao_lidas
    })
    return response