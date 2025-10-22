from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/gestor")
@requer_autenticacao(["gestor"])
async def get_gestor_home(request: Request, usuario_logado: dict = None):
    from data.repo import (
        unidade_coleta_repo, 
        gestor_repo, 
        doador_repo, 
        colaborador_repo, 
        notificacao_repo
    )
    
    # Buscar usuário do gestor para obter instituição
    gestor_atual = None
    if usuario_logado:
        gestor_atual = gestor_repo.obter_por_id(usuario_logado.get("cod_usuario", 0))
    
    # Buscar centros de coleta
    centros_coleta = unidade_coleta_repo.obter_todos()
    if centros_coleta is None:
        centros_coleta = []
    total_centros_coleta = len(centros_coleta) if centros_coleta else 0
    
    # Buscar administradores (gestores)
    todos_gestores = gestor_repo.obter_todos()
    if todos_gestores is None:
        todos_gestores = []
    total_administradores = len(todos_gestores)
    
    # Buscar doadores
    todos_doadores = doador_repo.obter_todos()
    if todos_doadores is None:
        todos_doadores = []
    total_doadores = len(todos_doadores)
    
    # Buscar colaboradores ativos
    todos_colaboradores = colaborador_repo.obter_todos()
    if todos_colaboradores is None:
        todos_colaboradores = []
    # Filtrar apenas colaboradores com status ativo (1)
    colaboradores_ativos = [c for c in todos_colaboradores if hasattr(c, 'status') and c.status == 1]
    total_colaboradores_ativos = len(colaboradores_ativos)
    
    # Buscar notificações recentes
    todas_notificacoes = notificacao_repo.obter_todos()
    if todas_notificacoes is None:
        todas_notificacoes = []
    notificacoes_recentes = sorted(todas_notificacoes, key=lambda x: x.data_envio if hasattr(x, 'data_envio') else datetime.now(), reverse=True)[:5] if todas_notificacoes else []
    
    # Limitar centros de coleta a 3 para a seção em destaque
    centros_coleta_destaque = centros_coleta[:3] if centros_coleta else []
    
    response = templates.TemplateResponse(
        "gestor/gestor_inicio.html", 
        {
            "request": request, 
            "usuario": usuario_logado,
            "active_page": "home",
            "centros_coleta": centros_coleta_destaque,
            "total_centros_coleta": total_centros_coleta,
            "total_administradores": total_administradores,
            "total_doadores": total_doadores,
            "total_colaboradores_ativos": total_colaboradores_ativos,
            "notificacoes_recentes": notificacoes_recentes,
            "now": datetime.now
        }
    )
    return response