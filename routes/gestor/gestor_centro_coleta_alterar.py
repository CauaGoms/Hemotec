from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from util.template_util import formatar_cpf, formatar_telefone, formatar_cep
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.filters['formatar_cpf'] = formatar_cpf
templates.env.filters['formatar_telefone'] = formatar_telefone
templates.env.filters['formatar_cep'] = formatar_cep

@router.get("/gestor/centro-coleta/alterar/{cod_unidade}")
@requer_autenticacao(["gestor"])
async def get_gestor_centro_coleta_alterar(request: Request, cod_unidade: int, usuario_logado: dict = None):
    try:
        print(f"=== ALTERAR CENTRO COLETA cod={cod_unidade} ===")
        from data.repo import unidade_coleta_repo, cidade_repo
        
        unidade = unidade_coleta_repo.obter_por_id(cod_unidade)
        print(f"Unidade: {unidade}")
        
        if not unidade:
            raise HTTPException(status_code=404, detail="Centro de coleta não encontrado")
        
        cidades = cidade_repo.obter_todos()
        print(f"Cidades: {len(cidades)}")
        
        response = templates.TemplateResponse(
            "gestor/gestor_centro_coleta_alterar.html",
            {
                "request": request,
                "active_page": "centro-coleta",
                "unidade": unidade,
                "cidades": cidades,
                "usuario": usuario_logado
            }
        )
        return response
    except Exception as e:
        print(f"!!! ERRO em alterar GET: {e}")
        import traceback
        traceback.print_exc()
        raise

@router.post("/api/gestor/centro-coleta/alterar/{cod_unidade}")
@requer_autenticacao(["gestor"])
async def post_gestor_centro_coleta_alterar(request: Request, cod_unidade: int, usuario_logado: dict = None):
    from data.repo import unidade_coleta_repo
    
    try:
        print(f"=== POST ALTERAR CENTRO COLETA cod={cod_unidade} ===")
        data = await request.json()
        print(f"Dados recebidos: {data}")
        
        unidade = unidade_coleta_repo.obter_por_id(cod_unidade)
        if not unidade:
            raise HTTPException(status_code=404, detail="Centro de coleta não encontrado")
        
        print(f"Unidade antes: {unidade}")
        
        # Atualizar dados da unidade
        unidade.nome = data['nome']
        unidade.email = data['email']
        unidade.telefone = data['telefone']
        unidade.rua_unidade = data['logradouro']
        unidade.bairro_unidade = data['bairro']
        unidade.cidade_unidade = int(data['cod_cidade'])
        unidade.cep_unidade = data['cep']
        
        print(f"Unidade depois: {unidade}")
        print("Chamando update()...")
        
        unidade_coleta_repo.update(unidade)
        
        print("Update OK!")
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Centro de coleta atualizado com sucesso!"
            },
            status_code=200
        )
        
    except Exception as e:
        print(f"!!! ERRO ao alterar centro: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao atualizar centro de coleta: {str(e)}"
            },
            status_code=500
        )