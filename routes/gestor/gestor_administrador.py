from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from util.template_util import formatar_cpf, formatar_telefone, formatar_cep

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.filters['formatar_cpf'] = formatar_cpf
templates.env.filters['formatar_telefone'] = formatar_telefone
templates.env.filters['formatar_cep'] = formatar_cep

@router.get("/gestor/administrador")
@requer_autenticacao(["gestor"])
async def gestor_administrador(request: Request, usuario_logado: dict = None):
    try:
        print("=== INICIANDO ROTA gestor_administrador ===")
        # Import dentro da função para evitar problemas de importação circular
        from data.repo import adm_unidade_repo
        print("Import de adm_unidade_repo OK")
        
        # Buscar todos os administradores do banco de dados
        print("Chamando obter_todos()...")
        administradores = adm_unidade_repo.obter_todos()
        print(f"Resultado: {len(administradores) if administradores else 0} administradores")
        if administradores is None:
            administradores = []
        
        print("Preparando template response...")
        response = templates.TemplateResponse("gestor/gestor_administrador.html", {
            "request": request,
            "active_page": "administrador",
            "administradores": administradores,
            "usuario": usuario_logado
        })
        print("Template response criado com sucesso!")
        return response
    except Exception as e:
        print(f"!!! ERRO ao carregar administradores: {e}")
        import traceback
        traceback.print_exc()
        raise