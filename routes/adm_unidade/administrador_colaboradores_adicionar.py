from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import colaborador_repo, cidade_repo, unidade_coleta_repo
from data.model.colaborador_model import Colaborador
from util.security import criar_hash_senha
from datetime import datetime, date

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/colaboradores/adicionar")
@requer_autenticacao(["administrador"])
async def get_administrador_colaboradores_adicionar(request: Request, usuario_logado: dict = None):
    # Buscar cidades e unidades para os selects do formulário
    cidades = cidade_repo.obter_todos()
    unidades = unidade_coleta_repo.obter_todos()
    
    response = templates.TemplateResponse(
        "adm_unidade/administrador_colaboradores_adicionar.html", 
        {
            "request": request, 
            "active_page": "colaborador",
            "usuario": usuario_logado,
            "cidades": cidades,
            "unidades": unidades
        }
    )
    return response

@router.post("/api/administrador/colaboradores/adicionar")
@requer_autenticacao(["administrador"])
async def post_administrador_colaboradores_adicionar(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    telefone: str = Form(...),
    rua_usuario: str = Form(...),
    bairro_usuario: str = Form(...),
    cidade_usuario: int = Form(...),
    cep_usuario: str = Form(...),
    cod_unidade: int = Form(...),
    funcao: str = Form(""),
    usuario_logado: dict = None
):
    """Adiciona um novo colaborador ao banco de dados"""
    try:
        # Criptografar senha
        senha_criptografada = criar_hash_senha(senha)
        
        # Criar objeto Colaborador
        colaborador = Colaborador(
            cod_colaborador=0,  # Será gerado pelo banco
            cod_usuario=0,  # Será gerado pelo banco
            cod_unidade=cod_unidade,
            nome=nome,
            email=email,
            senha=senha_criptografada,
            cpf=cpf,
            data_nascimento=datetime.strptime(data_nascimento, "%Y-%m-%d").date(),
            status=True,  # Novo colaborador começa ativo
            data_cadastro=date.today(),
            rua_usuario=rua_usuario,
            bairro_usuario=bairro_usuario,
            cidade_usuario=cidade_usuario,
            cep_usuario=cep_usuario,
            telefone=telefone,
            funcao=funcao
        )
        
        # Inserir colaborador no banco
        cod_colaborador = colaborador_repo.inserir(colaborador)
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Colaborador criado com sucesso!",
                "cod_colaborador": cod_colaborador
            },
            status_code=201
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao criar colaborador: {str(e)}"
            },
            status_code=500
        )