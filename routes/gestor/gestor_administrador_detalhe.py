from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from util.template_util import formatar_cpf, formatar_telefone, formatar_cep

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.filters['formatar_cpf'] = formatar_cpf
templates.env.filters['formatar_telefone'] = formatar_telefone
templates.env.filters['formatar_cep'] = formatar_cep

@router.get("/gestor/administrador/detalhe/{cod_administrador}")
@requer_autenticacao(["gestor"])
async def gestor_administrador_detalhe(request: Request, cod_administrador: int, usuario_logado: dict = None):
    try:
        print(f"=== DETALHE ADMINISTRADOR cod={cod_administrador} ===")
        from data.repo import adm_unidade_repo, cidade_repo, unidade_coleta_repo
        # Buscar administrador específico do banco de dados
        administrador = adm_unidade_repo.obter_por_id(cod_administrador)
        print(f"Administrador: {administrador}")
        
        if not administrador:
            raise HTTPException(status_code=404, detail="Administrador não encontrado")
        
        # Buscar cidade e unidade do administrador
        print(f"Buscando cidade: {administrador.cidade_usuario}")
        cidade = cidade_repo.obter_por_id(administrador.cidade_usuario)
        print(f"Cidade: {cidade}")
        
        print(f"Buscando unidade: {administrador.cod_unidade}")
        unidade = unidade_coleta_repo.obter_por_id(administrador.cod_unidade)
        print(f"Unidade: {unidade}")
        
        response = templates.TemplateResponse("gestor/gestor_administrador_detalhe.html", {
            "request": request, 
            "active_page": "administrador",
            "administrador": administrador,
            "cidade": cidade,
            "unidade": unidade,
            "usuario": usuario_logado
        })
        return response
    except Exception as e:
        print(f"!!! ERRO em detalhe: {e}")
        import traceback
        traceback.print_exc()
        raise