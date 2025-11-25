from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from util.template_util import formatar_cpf, formatar_telefone, formatar_cep

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.filters['formatar_cpf'] = formatar_cpf
templates.env.filters['formatar_telefone'] = formatar_telefone
templates.env.filters['formatar_cep'] = formatar_cep

@router.get("/gestor/centro-coleta")
@requer_autenticacao(["gestor"])
async def gestor_centro_coleta(request: Request, usuario_logado: dict = None):
    try:
        print("=== INICIANDO ROTA gestor_centro_coleta ===")
        from data.repo import unidade_coleta_repo
        print("Import de unidade_coleta_repo OK")
        
        # Get search parameters
        search = request.query_params.get('search', '')
        cidade_filter = request.query_params.get('cidade', '')
        status_filter = request.query_params.get('status', '')
        
        print(f"Filtros - search: {search}, cidade: {cidade_filter}, status: {status_filter}")
        print("Chamando obter_todos()...")
        
        unidades = unidade_coleta_repo.obter_todos()
        print(f"Resultado: {len(unidades)} centros de coleta")
        
        # Apply filters
        if search:
            unidades = [u for u in unidades if search.lower() in u.nome.lower() or 
                       (u.email and search.lower() in u.email.lower())]
        
        if cidade_filter:
            unidades = [u for u in unidades if u.cidade_unidade == int(cidade_filter)]
        
        # Get cidades for filter
        from data.repo import cidade_repo
        cidades = cidade_repo.obter_todos()
        
        print("Preparando template response...")
        response = templates.TemplateResponse(
            "gestor/gestor_centro_coleta.html",
            {
                "request": request,
                "active_page": "centro-coleta",
                "unidades": unidades,
                "cidades": cidades,
                "usuario": usuario_logado,
                "search": search,
                "cidade_filter": cidade_filter,
                "status_filter": status_filter
            }
        )
        print("Template response criado com sucesso!")
        return response
        
    except Exception as e:
        print(f"!!! ERRO em gestor_centro_coleta: {e}")
        import traceback
        traceback.print_exc()
        raise