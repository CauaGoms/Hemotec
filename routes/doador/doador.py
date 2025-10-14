from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import doador_repo, notificacao_repo, campanha_repo
from util.auth_decorator import requer_autenticacao
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador")
@requer_autenticacao(["doador"])
async def get_doador_home(request: Request, usuario_logado: dict = None):
    # Buscar as 3 notificações mais recentes (gerais, não filtradas por usuário)
    todas_notificacoes = notificacao_repo.obter_todos()
    # Ordena por data_envio DESC e pega as 3 mais recentes
    notificacoes_recentes = sorted(todas_notificacoes, key=lambda x: x.data_envio, reverse=True)[:3]
    # Conta notificações não lidas (status = 1)
    total_nao_lidas = sum(1 for n in todas_notificacoes if n.status == 1)
    
    # Buscar campanhas ativas
    todas_campanhas = campanha_repo.obter_todos()
    hoje = datetime.now().date()
    
    # Filtrar apenas campanhas ativas (data_fim >= hoje e data_inicio <= hoje)
    campanhas_ativas = [c for c in todas_campanhas if c.data_inicio <= hoje and c.data_fim >= hoje]
    
    # Ordenar por data_inicio (mais recentes primeiro) e limitar a 3
    campanhas_ativas = sorted(campanhas_ativas, key=lambda x: x.data_inicio, reverse=True)[:3]
    
    response = templates.TemplateResponse("doador/doador_inicio.html", {
        "request": request, 
        "active_page": "home", 
        "usuario": usuario_logado,
        "notificacoes_recentes": notificacoes_recentes,
        "total_nao_lidas": total_nao_lidas,
        "campanhas_ativas": campanhas_ativas,
        "total_campanhas_ativas": len([c for c in todas_campanhas if c.data_inicio <= hoje and c.data_fim >= hoje]),
        "now": datetime.now
    })
    return response