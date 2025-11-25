from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.model.unidade_coleta_model import Unidade_coleta
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/gestor/centro-coleta/adicionar")
@requer_autenticacao(["gestor"])
async def get_gestor_centro_coleta_adicionar(request: Request, usuario_logado: dict = None):
    try:
        from data.repo import cidade_repo
        cidades = cidade_repo.obter_todos()
        
        response = templates.TemplateResponse(
            "gestor/gestor_centro_coleta_adicionar.html",
            {
                "request": request,
                "active_page": "centro-coleta",
                "cidades": cidades,
                "usuario": usuario_logado
            }
        )
        return response
    except Exception as e:
        print(f"!!! ERRO em adicionar GET: {e}")
        import traceback
        traceback.print_exc()
        raise

@router.post("/api/gestor/centro-coleta/adicionar")
@requer_autenticacao(["gestor"])
async def post_gestor_centro_coleta_adicionar(request: Request, usuario_logado: dict = None):
    from data.repo import unidade_coleta_repo
    
    try:
        print("=== POST ADICIONAR CENTRO COLETA ===")
        data = await request.json()
        print(f"Dados recebidos: {data}")
        
        # Criar nova unidade de coleta
        nova_unidade = Unidade_coleta(
            cod_unidade=None,
            cod_licenca=1,  # Licença padrão
            cod_horario_funcionamento=1,  # Horário padrão (08:00-17:00)
            nome=data['nome'],
            email=data.get('email') or 'contato@centro.com',  # Email padrão se não fornecido
            rua_unidade=data['logradouro'],
            bairro_unidade=data['bairro'],
            cidade_unidade=int(data['cod_cidade']),
            cep_unidade=data['cep'],
            latitude=0.0,  # Coordenadas padrão (pode ser atualizado posteriormente)
            longitude=0.0,  # Coordenadas padrão (pode ser atualizado posteriormente)
            telefone=data['telefone']
        )
        
        print(f"Nova unidade: {nova_unidade}")
        print("Chamando inserir()...")
        
        unidade_coleta_repo.inserir(nova_unidade)
        
        print("Inserção OK!")
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Centro de coleta adicionado com sucesso!"
            },
            status_code=200
        )
        
    except Exception as e:
        print(f"!!! ERRO ao adicionar centro: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao adicionar centro de coleta: {str(e)}"
            },
            status_code=500
        )