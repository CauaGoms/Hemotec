from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.model.adm_unidade_model import Adm_unidade
from util.security import criar_hash_senha
from datetime import datetime, date
from util.template_util import formatar_cpf, formatar_telefone, formatar_cep

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.filters['formatar_cpf'] = formatar_cpf
templates.env.filters['formatar_telefone'] = formatar_telefone
templates.env.filters['formatar_cep'] = formatar_cep

@router.get("/gestor/administrador/adicionar")
@requer_autenticacao(["gestor"])
async def get_gestor_administrador_adicionar(request: Request, usuario_logado: dict = None):
    from data.repo import cidade_repo, unidade_coleta_repo
    
    # Buscar cidades e unidades para os selects do formulário
    cidades = cidade_repo.obter_todos()
    unidades = unidade_coleta_repo.obter_todos()
    
    response = templates.TemplateResponse(
        "gestor/gestor_administrador_adicionar.html", 
        {
            "request": request, 
            "active_page": "administrador",
            "usuario": usuario_logado,
            "cidades": cidades,
            "unidades": unidades
        }
    )
    return response

@router.post("/api/gestor/administrador/adicionar")
@requer_autenticacao(["gestor"])
async def post_gestor_administrador_adicionar(
    request: Request,
    usuario_logado: dict = None
):
    """Adiciona um novo administrador de unidade ao banco de dados"""
    from data.repo import adm_unidade_repo
    
    try:
        # Receber dados do JSON
        data = await request.json()
        print(f"=== DADOS RECEBIDOS: {data}")
        
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        cpf = data.get('cpf')
        data_nascimento = data.get('data_nascimento')
        telefone = data.get('telefone')
        rua_usuario = data.get('logradouro')  # Note: o campo no form é 'logradouro'
        bairro_usuario = data.get('bairro')
        cidade_usuario = int(data.get('cod_cidade'))
        cep_usuario = data.get('cep')
        cod_unidade = int(data.get('cod_unidade'))
        permissao_envio_campanha = data.get('permissao_envio_campanha', False)
        permissao_envio_notificacao = data.get('permissao_envio_notificacao', False)
        # Criptografar senha
        senha_criptografada = criar_hash_senha(senha)
        
        # Criar objeto Adm_unidade
        administrador = Adm_unidade(
            cod_adm=0,  # Será gerado pelo banco
            cod_unidade=cod_unidade,
            nome=nome,
            email=email,
            senha=senha_criptografada,
            cpf=cpf,
            data_nascimento=datetime.strptime(data_nascimento, "%Y-%m-%d").date(),
            status=True,  # Novo administrador começa ativo
            data_cadastro=date.today(),
            rua_usuario=rua_usuario,
            bairro_usuario=bairro_usuario,
            cidade_usuario=cidade_usuario,
            cep_usuario=cep_usuario,
            telefone=telefone,
            permissao_envio_campanha=permissao_envio_campanha,
            permissao_envio_notificacao=permissao_envio_notificacao
        )
        
        # Inserir administrador no banco
        print(f"=== INSERINDO ADMINISTRADOR: {administrador}")
        cod_administrador = adm_unidade_repo.inserir(administrador)
        print(f"=== COD ADMINISTRADOR CRIADO: {cod_administrador}")
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Administrador criado com sucesso!",
                "cod_administrador": cod_administrador
            },
            status_code=201
        )
        
    except Exception as e:
        print(f"!!! ERRO AO CRIAR ADMINISTRADOR: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao criar administrador: {str(e)}"
            },
            status_code=500
        )