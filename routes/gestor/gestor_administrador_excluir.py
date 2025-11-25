from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/gestor/administrador/excluir/{cod_administrador}")
@requer_autenticacao(["gestor"])
async def gestor_administrador_excluir_get(request: Request, cod_administrador: int, usuario_logado: dict = None):
    from data.repo import adm_unidade_repo, unidade_coleta_repo
    administrador = adm_unidade_repo.obter_por_id(cod_administrador)
    
    if not administrador:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    
    response = templates.TemplateResponse(
        "gestor/gestor_administrador_excluir.html", 
        {
            "request": request, 
            "active_page": "administrador",
            "administrador": administrador,
            "usuario": usuario_logado
        }
    )
    return response

@router.delete("/api/gestor/administrador/excluir/{cod_administrador}")
@requer_autenticacao(["gestor"])
async def delete_gestor_administrador_excluir(request: Request, cod_administrador: int, usuario_logado: dict = None):
    from data.repo import adm_unidade_repo
    
    try:
        administrador = adm_unidade_repo.obter_por_id(cod_administrador)
        if not administrador:
            raise HTTPException(status_code=404, detail="Administrador não encontrado")
        
        adm_unidade_repo.delete(cod_administrador)
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Administrador excluído com sucesso!"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao excluir administrador: {str(e)}"
            },
            status_code=500
        )