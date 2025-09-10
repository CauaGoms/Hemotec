from datetime import datetime
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data.model.cidade_model import Cidade
from data.model.usuario_model import Usuario
from data.repo import cidade_repo, usuario_repo
from util.auth_decorator import criar_sessao, requer_autenticacao
from util.security import criar_hash_senha, verificar_senha

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Rota de login
@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    usuario = usuario_repo.obter_por_email(email)

    if not usuario or not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse(
            "publico/publico_login.html",
            {"request": request, "erro": "Email ou senha inválidos"}
        )

    # Criar sessão
    usuario_dict = {
        "cod_usuario": usuario.cod_usuario,
        "nome": usuario.nome,
        "email": usuario.email,
        "cpf": usuario.cpf,
        "data_nascimento": usuario.data_nascimento,
        "status": usuario.status,
        "rua_usuario": usuario.rua_usuario,
        "bairro_usuario": usuario.bairro_usuario,
        "cidade_usuario": usuario.cidade_usuario,
        "cep_usuario": usuario.cep_usuario,
        "telefone": usuario.telefone,
        "perfil": usuario.perfil,
        "foto": usuario.foto,
        "estado_usuario": usuario.estado_usuario
    }
    criar_sessao(request, usuario_dict)
    print(usuario_dict)

    # Redirecionar
    if redirect:
        return RedirectResponse(redirect, status.HTTP_303_SEE_OTHER)

    if usuario.perfil and usuario.perfil.strip().lower() == "doador":
        return RedirectResponse("/doador", status.HTTP_303_SEE_OTHER)

    if usuario.perfil and usuario.perfil.strip().lower() == "gestor":
        return RedirectResponse("/gestor", status.HTTP_303_SEE_OTHER)

    if usuario.perfil and usuario.perfil.strip().lower() == "administrador":
        return RedirectResponse("/administrador", status.HTTP_303_SEE_OTHER)

    if usuario.perfil and usuario.perfil.strip().lower() == "colaborador":
        return RedirectResponse("/colaborador", status.HTTP_303_SEE_OTHER)

    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

@router.get("/usuario/sair")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

@router.post("/cadastrar")
async def post_cadastro(
    request: Request,
    nome: str = Form(...),
    cpf: str = Form(...),
    data_nascimento: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cep_usuario: str = Form(...),
    rua_usuario: str = Form(...),
    bairro_usuario: str = Form(...),
    cidade_usuario: str = Form(...),
    estado_usuario: str = Form(...),
    senha: str = Form(...)
):
    print(f"estado: {estado_usuario}")
    # Verificar se email já existe
    if usuario_repo.obter_por_email(email):
        print("Email já cadastrado")
        return templates.TemplateResponse(
            "publico/publico_cadastrar_doador.html",
            {"request": request, "erro": "Email já cadastrado"}
        )
    
    # Criar hash da senha
    senha_hash = criar_hash_senha(senha)
    
    # Criar usuário
    usuario = Usuario(
        cod_usuario=0,
        nome=nome,
        email=email,
        senha=senha_hash,
        cpf=cpf,
        data_nascimento=data_nascimento,
        status=True,
        rua_usuario=rua_usuario,
        bairro_usuario=bairro_usuario,
        cidade_usuario=cidade_usuario,
        cep_usuario=cep_usuario,
        telefone=telefone,
        perfil="doador",
        data_cadastro=None,
        estado_usuario=estado_usuario
    )

    # cidade_repo.inserir(Cidade(cod_cidade=0, nome_cidade=cidade_usuario, sigla_estado=estado_usuario))
    # usuario_repo.inserir(usuario)

    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)

# Rota acessível apenas para usuários logados
@router.get("/dados_cadastrais")
@requer_autenticacao()
async def get_dados_cadastrais(request: Request, usuario_logado: dict = None):
    # usuario_logado contém os dados do usuário
    return templates.TemplateResponse(
        "dados_cadastrais.html",
        {"request": request, "usuario": usuario_logado}
    )

# Rota apenas para gestores
@router.get("/gestor")
@requer_autenticacao(["gestor"])
async def get_gestor_dashboard(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse(
        "gestor_inicio.html",
        {"request": request}
    )

# Rota apenas para administradores de unidade
@router.get("/administrador")
@requer_autenticacao(["administrador"])
async def get_administrador_dashboard(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse(
        "administrador_inicio.html",
        {"request": request}
    )

# Rota apenas para colaboradores
@router.get("/colaborador")
@requer_autenticacao(["colaborador"])
async def get_colaborador_dashboard(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse(
        "colaborador_inicio.html",
        {"request": request}
    )

# Rota apenas para doadores
@router.get("/doador")
@requer_autenticacao(["doador"])
async def get_doador_dashboard(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse(
        "doador_inicio.html",
        {"request": request}
    )

# # Rota para múltiplos perfis
# @router.get("/relatorios")
# @requer_autenticacao(["admin", "gerente"])
# async def get_relatorios(request: Request, usuario_logado: dict = None):
#     return templates.TemplateResponse(
#         "relatorios.html",
#         {"request": request}
#     )