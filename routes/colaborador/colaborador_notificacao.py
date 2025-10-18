from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from data.repo import notificacao_repo
from util.auth_decorator import requer_autenticacao
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/notificacao")
@requer_autenticacao(["colaborador"])
async def get_colaborador_notificacao(request: Request, usuario_logado: dict = None):
    notificacoes = notificacao_repo.obter_todos()
    response = templates.TemplateResponse(
        "colaborador/colaborador_notificacao.html",
        {
            "request": request, 
            "active_page": "notificacao", 
            "usuario": usuario_logado, 
            "notificacoes": notificacoes
        }
    )
    return response

@router.get("/api/colaborador/notificacoes")
@requer_autenticacao(["colaborador"])
async def get_colaborador_notificacoes_api(request: Request, usuario_logado: dict = None):
    """Retorna todas as notificações em formato JSON"""
    notificacoes = notificacao_repo.obter_todos()
    return JSONResponse(content={
        "notificacoes": [
            {
                "cod_notificacao": n.cod_notificacao,
                "tipo": n.tipo,
                "titulo": n.titulo,
                "mensagem": n.mensagem,
                "status": n.status,
                "data_envio": n.data_envio.strftime('%Y-%m-%d %H:%M:%S') if isinstance(n.data_envio, datetime) else str(n.data_envio)
            }
            for n in notificacoes
        ]
    })

@router.get("/api/colaborador/notificacoes/nao-lidas")
@requer_autenticacao(["colaborador"])
async def get_colaborador_notificacoes_nao_lidas(request: Request, usuario_logado: dict = None):
    """Retorna as últimas 2 notificações não lidas e o contador total"""
    cod_usuario = usuario_logado["cod_usuario"]
    notificacoes = notificacao_repo.obter_ultimas_nao_lidas(cod_usuario, 2)
    total_nao_lidas = notificacao_repo.contar_nao_lidas(cod_usuario)
    return JSONResponse(content={
        "total": total_nao_lidas,
        "notificacoes": [
            {
                "cod_notificacao": n.cod_notificacao,
                "tipo": n.tipo,
                "titulo": n.titulo,
                "mensagem": n.mensagem,
                "status": n.status,
                "data_envio": n.data_envio.strftime('%Y-%m-%d %H:%M:%S') if isinstance(n.data_envio, datetime) else str(n.data_envio)
            }
            for n in notificacoes
        ]
    })

@router.post("/api/colaborador/notificacoes/{cod_notificacao}/marcar-lida")
@requer_autenticacao(["colaborador"])
async def marcar_colaborador_notificacao_lida(cod_notificacao: int, request: Request, usuario_logado: dict = None):
    """Marca uma notificação como lida (status = 0)"""
    notificacao = notificacao_repo.obter_por_id(cod_notificacao)
    if notificacao:
        notificacao.status = 0
        sucesso = notificacao_repo.update(notificacao)
        return JSONResponse(content={"success": sucesso})
    return JSONResponse(content={"success": False, "error": "Notificação não encontrada"}, status_code=404)

@router.post("/api/colaborador/notificacoes/marcar-todas-lidas")
@requer_autenticacao(["colaborador"])
async def marcar_colaborador_todas_lidas(request: Request, usuario_logado: dict = None):
    """Marca todas as notificações como lidas"""
    notificacoes = notificacao_repo.obter_todos()
    sucesso_total = True
    for notificacao in notificacoes:
        if notificacao.status == 1:
            notificacao.status = 0
            sucesso = notificacao_repo.update(notificacao)
            if not sucesso:
                sucesso_total = False
    return JSONResponse(content={"success": sucesso_total})

@router.delete("/api/colaborador/notificacoes/{cod_notificacao}")
@requer_autenticacao(["colaborador"])
async def deletar_colaborador_notificacao(cod_notificacao: int, request: Request, usuario_logado: dict = None):
    """Deleta uma notificação"""
    sucesso = notificacao_repo.delete(cod_notificacao)
    return JSONResponse(content={"success": sucesso})

@router.delete("/api/colaborador/notificacoes/limpar-todas")
@requer_autenticacao(["colaborador"])
async def limpar_todas_colaborador_notificacoes(request: Request, usuario_logado: dict = None):
    """Deleta todas as notificações"""
    notificacoes = notificacao_repo.obter_todos()
    sucesso_total = True
    for notificacao in notificacoes:
        sucesso = notificacao_repo.delete(notificacao.cod_notificacao)
        if not sucesso:
            sucesso_total = False
    return JSONResponse(content={"success": sucesso_total})
