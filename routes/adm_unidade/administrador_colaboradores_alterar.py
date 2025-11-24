from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import colaborador_repo, cidade_repo, unidade_coleta_repo
from data.model.colaborador_model import Colaborador
from util.security import criar_hash_senha
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/colaboradores/alterar/{cod_colaborador}")
@requer_autenticacao(["administrador"])
async def get_administrador_colaboradores_alterar(request: Request, cod_colaborador: int, usuario_logado: dict = None):
    colaborador = colaborador_repo.obter_por_id(cod_colaborador)
    
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    
    cidades = cidade_repo.obter_todos()
    unidades = unidade_coleta_repo.obter_todos()
    
    response = templates.TemplateResponse(
        "adm_unidade/administrador_colaboradores_alterar.html", 
        {
            "request": request, 
            "active_page": "colaborador",
            "colaborador": colaborador,
            "cidades": cidades,
            "unidades": unidades,
            "usuario": usuario_logado
        }
    )
    return response

@router.post("/api/administrador/colaboradores/alterar/{cod_colaborador}")
@requer_autenticacao(["administrador"])
async def post_administrador_colaboradores_alterar(
    request: Request,
    cod_colaborador: int,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    telefone: str = Form(...),
    rua_usuario: str = Form(...),
    bairro_usuario: str = Form(...),
    cidade_usuario: int = Form(...),
    cep_usuario: str = Form(...),
    cod_unidade: int = Form(...),
    funcao: str = Form(""),
    status: bool = Form(True),
    senha: str = Form(None),
    usuario_logado: dict = None
):
    try:
        colaborador = colaborador_repo.obter_por_id(cod_colaborador)
        if not colaborador:
            raise HTTPException(status_code=404, detail="Colaborador não encontrado")
        
        # Atualizar senha apenas se fornecida
        if senha and senha.strip():
            colaborador.senha = criar_hash_senha(senha)
        
        # Atualizar dados
        colaborador.nome = nome
        colaborador.email = email
        colaborador.cpf = cpf
        colaborador.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        colaborador.telefone = telefone
        colaborador.rua_usuario = rua_usuario
        colaborador.bairro_usuario = bairro_usuario
        colaborador.cidade_usuario = cidade_usuario
        colaborador.cep_usuario = cep_usuario
        colaborador.cod_unidade = cod_unidade
        colaborador.funcao = funcao
        colaborador.status = status
        
        colaborador_repo.update(colaborador)
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Colaborador atualizado com sucesso!"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao atualizar colaborador: {str(e)}"
            },
            status_code=500
        )