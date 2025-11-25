from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.model.adm_unidade_model import Adm_unidade
from util.security import criar_hash_senha
from datetime import datetime
from util.template_util import formatar_cpf, formatar_telefone, formatar_cep

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.filters['formatar_cpf'] = formatar_cpf
templates.env.filters['formatar_telefone'] = formatar_telefone
templates.env.filters['formatar_cep'] = formatar_cep

@router.get("/gestor/administrador/alterar/{cod_administrador}")
@requer_autenticacao(["gestor"])
async def get_gestor_administrador_alterar(request: Request, cod_administrador: int, usuario_logado: dict = None):
    try:
        print(f"=== ALTERAR ADMINISTRADOR cod={cod_administrador} ===")
        from data.repo import adm_unidade_repo, cidade_repo, unidade_coleta_repo
        administrador = adm_unidade_repo.obter_por_id(cod_administrador)
        print(f"Administrador: {administrador}")
        
        if not administrador:
            raise HTTPException(status_code=404, detail="Administrador não encontrado")
        
        cidades = cidade_repo.obter_todos()
        unidades = unidade_coleta_repo.obter_todos()
        print(f"Cidades: {len(cidades)}, Unidades: {len(unidades)}")
        
        response = templates.TemplateResponse(
            "gestor/gestor_administrador_alterar.html", 
            {
                "request": request, 
                "active_page": "administrador",
                "administrador": administrador,
                "cidades": cidades,
                "unidades": unidades,
                "usuario": usuario_logado
            }
        )
        return response
    except Exception as e:
        print(f"!!! ERRO em alterar GET: {e}")
        import traceback
        traceback.print_exc()
        raise

@router.post("/api/gestor/administrador/alterar/{cod_administrador}")
@requer_autenticacao(["gestor"])
async def post_gestor_administrador_alterar(
    request: Request,
    cod_administrador: int,
    usuario_logado: dict = None
):
    from data.repo import adm_unidade_repo
    
    try:
        print(f"=== POST ALTERAR ADMINISTRADOR cod={cod_administrador} ===")
        # Get JSON data from request
        data = await request.json()
        print(f"Dados recebidos: {data}")
        
        administrador = adm_unidade_repo.obter_por_id(cod_administrador)
        if not administrador:
            raise HTTPException(status_code=404, detail="Administrador não encontrado")
        
        print(f"Administrador antes: {administrador}")
        
        # Se forneceu uma nova senha, criptografa
        if data.get('senha') and data.get('change_password'):
            administrador.senha = criar_hash_senha(data['senha'])
        
        # Atualizar dados do administrador
        administrador.nome = data['nome']
        administrador.email = data['email']
        administrador.cpf = data['cpf']
        administrador.data_nascimento = datetime.strptime(data['data_nascimento'], "%Y-%m-%d").date()
        administrador.telefone = data['telefone']
        administrador.rua_usuario = data['logradouro']
        administrador.bairro_usuario = data['bairro']
        administrador.cidade_usuario = int(data['cod_cidade'])
        administrador.cep_usuario = data['cep']
        administrador.cod_unidade = int(data['cod_unidade'])
        administrador.permissao_envio_campanha = data.get('permissao_envio_campanha', False)
        administrador.permissao_envio_notificacao = data.get('permissao_envio_notificacao', False)
        administrador.status = 1 if data.get('status', True) else 0
        
        print(f"Administrador depois: {administrador}")
        print("Chamando update()...")
        
        # Atualizar no banco
        adm_unidade_repo.update(administrador)
        
        print("Update OK!")
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Administrador atualizado com sucesso!"
            },
            status_code=200
        )
        
    except Exception as e:
        print(f"!!! ERRO ao alterar administrador: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao atualizar administrador: {str(e)}"
            },
            status_code=500
        )