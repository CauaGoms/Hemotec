from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from data.repo import notificacao_repo
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/notificacao")
async def administrador_notificacao(request: Request):
    notificacoes = notificacao_repo.obter_todos()
    response = templates.TemplateResponse(
        "adm_unidade/administrador_notificacao.html",
        {
            "request": request, 
            "active_page": "notificacao", 
            "notificacoes": notificacoes
        }
    )
    return response

@router.get("/api/administrador/notificacoes")
async def get_administrador_notificacoes_api(request: Request):
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

@router.get("/api/administrador/notificacoes/nao-lidas")
async def get_administrador_notificacoes_nao_lidas(request: Request):
    """Retorna as últimas 2 notificações não lidas e o contador total"""
    notificacoes = notificacao_repo.obter_todos()
    nao_lidas = [n for n in notificacoes if n.status == 1][:2]
    total_nao_lidas = len([n for n in notificacoes if n.status == 1])
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
            for n in nao_lidas
        ]
    })

@router.post("/api/administrador/notificacoes/{cod_notificacao}/marcar-lida")
async def marcar_administrador_notificacao_lida(cod_notificacao: int, request: Request):
    """Marca uma notificação como lida (status = 0)"""
    notificacao = notificacao_repo.obter_por_id(cod_notificacao)
    if notificacao:
        notificacao.status = 0
        sucesso = notificacao_repo.update(notificacao)
        return JSONResponse(content={"success": sucesso})
    return JSONResponse(content={"success": False, "error": "Notificação não encontrada"}, status_code=404)

@router.post("/api/administrador/notificacoes/marcar-todas-lidas")
async def marcar_administrador_todas_lidas(request: Request):
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

@router.delete("/api/administrador/notificacoes/{cod_notificacao}")
async def deletar_administrador_notificacao(cod_notificacao: int, request: Request):
    """Deleta uma notificação"""
    sucesso = notificacao_repo.delete(cod_notificacao)
    return JSONResponse(content={"success": sucesso})

@router.delete("/api/administrador/notificacoes/limpar-todas")
async def limpar_todas_administrador_notificacoes(request: Request):
    """Deleta todas as notificações"""
    notificacoes = notificacao_repo.obter_todos()
    sucesso_total = True
    for notificacao in notificacoes:
        sucesso = notificacao_repo.delete(notificacao.cod_notificacao)
        if not sucesso:
            sucesso_total = False
    return JSONResponse(content={"success": sucesso_total})