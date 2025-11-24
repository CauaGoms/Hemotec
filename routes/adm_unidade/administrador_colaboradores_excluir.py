from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import colaborador_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/colaboradores/excluir/{cod_colaborador}")
@requer_autenticacao(["administrador"])
async def get_administrador_colaboradores_excluir(request: Request, cod_colaborador: int, usuario_logado: dict = None):
    colaborador = colaborador_repo.obter_por_id(cod_colaborador)
    
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    
    response = templates.TemplateResponse(
        "adm_unidade/administrador_colaboradores_excluir.html", 
        {
            "request": request, 
            "active_page": "colaborador",
            "colaborador": colaborador,
            "usuario": usuario_logado
        }
    )
    return response

@router.delete("/api/administrador/colaboradores/excluir/{cod_colaborador}")
@requer_autenticacao(["administrador"])
async def delete_administrador_colaboradores_excluir(request: Request, cod_colaborador: int, usuario_logado: dict = None):
    try:
        colaborador = colaborador_repo.obter_por_id(cod_colaborador)
        if not colaborador:
            raise HTTPException(status_code=404, detail="Colaborador não encontrado")
        
        colaborador_repo.delete(cod_colaborador)
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Colaborador excluído com sucesso!"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao excluir colaborador: {str(e)}"
            },
            status_code=500
        )