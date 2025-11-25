from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from util.template_util import formatar_cpf, formatar_telefone, formatar_cep

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.filters['formatar_cpf'] = formatar_cpf
templates.env.filters['formatar_telefone'] = formatar_telefone
templates.env.filters['formatar_cep'] = formatar_cep

@router.get("/gestor/centro-coleta/detalhe/{cod_unidade}")
@requer_autenticacao(["gestor"])
async def gestor_centro_coleta_detalhe(request: Request, cod_unidade: int, usuario_logado: dict = None):
    try:
        from data.repo import unidade_coleta_repo, cidade_repo
        
        unidade = unidade_coleta_repo.obter_por_id(cod_unidade)
        
        if not unidade:
            raise HTTPException(status_code=404, detail="Centro de coleta não encontrado")
        
        # Get cidade info
        cidade = None
        if unidade.cidade_unidade:
            cidade = cidade_repo.obter_por_id(unidade.cidade_unidade)
        
        response = templates.TemplateResponse(
            "gestor/gestor_centro_coleta_detalhe.html",
            {
                "request": request,
                "active_page": "centro-coleta",
                "unidade": unidade,
                "cidade": cidade,
                "usuario": usuario_logado
            }
        )
        return response
        
    except Exception as e:
        print(f"!!! ERRO em detalhe: {e}")
        import traceback
        traceback.print_exc()
        raise