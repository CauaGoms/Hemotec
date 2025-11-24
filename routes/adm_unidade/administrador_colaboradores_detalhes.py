from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from data.repo import colaborador_repo, cidade_repo, unidade_coleta_repo
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/colaboradores/detalhes/{cod_colaborador}")
@requer_autenticacao(["administrador"])
async def administrador_colaboradores_detalhes(request: Request, cod_colaborador: int, usuario_logado: dict = None):
    # Buscar colaborador específico do banco de dados
    colaborador = colaborador_repo.obter_por_id(cod_colaborador)
    
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    
    # Buscar cidade e unidade do colaborador
    cidade = cidade_repo.obter_por_id(colaborador.cidade_usuario)
    unidade = unidade_coleta_repo.obter_por_id(colaborador.cod_unidade)
    
    response = templates.TemplateResponse("adm_unidade/administrador_colaboradores_detalhes.html", {
        "request": request, 
        "active_page": "colaborador",
        "colaborador": colaborador,
        "cidade": cidade,
        "unidade": unidade,
        "usuario": usuario_logado
    })
    return response