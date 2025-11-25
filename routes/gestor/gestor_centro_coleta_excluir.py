from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/gestor/centro-coleta/excluir/{cod_unidade}")
@requer_autenticacao(["gestor"])
async def gestor_centro_coleta_excluir_get(request: Request, cod_unidade: int, usuario_logado: dict = None):
    from data.repo import unidade_coleta_repo
    unidade = unidade_coleta_repo.obter_por_id(cod_unidade)
    
    if not unidade:
        raise HTTPException(status_code=404, detail="Centro de coleta não encontrado")
    
    response = templates.TemplateResponse(
        "gestor/gestor_centro_coleta_excluir.html",
        {
            "request": request,
            "active_page": "centro-coleta",
            "unidade": unidade,
            "usuario": usuario_logado
        }
    )
    return response

@router.delete("/api/gestor/centro-coleta/excluir/{cod_unidade}")
@requer_autenticacao(["gestor"])
async def delete_gestor_centro_coleta_excluir(request: Request, cod_unidade: int, usuario_logado: dict = None):
    from data.repo import unidade_coleta_repo
    
    try:
        unidade = unidade_coleta_repo.obter_por_id(cod_unidade)
        if not unidade:
            raise HTTPException(status_code=404, detail="Centro de coleta não encontrado")
        
        unidade_coleta_repo.delete(cod_unidade)
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Centro de coleta excluído com sucesso!"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao excluir centro de coleta: {str(e)}"
            },
            status_code=500
        )