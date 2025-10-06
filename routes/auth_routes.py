from datetime import datetime
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic_core import ValidationError
import sqlite3
from data.model.cidade_model import Cidade
from data.model.usuario_model import Usuario
from data.repo import cidade_repo, usuario_repo
from dtos.usuario_dtos import CriarUsuarioDTO
from util.auth_decorator import criar_sessao, requer_autenticacao
from util.flash_messages import informar_sucesso, informar_erro
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
        "data_nascimento": str(usuario.data_nascimento),
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
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
):
    dados_formulario = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "email": email,
        "telefone": telefone,
        "cep_usuario": cep_usuario,
        "rua_usuario": rua_usuario,
        "bairro_usuario": bairro_usuario,
        "cidade_usuario": cidade_usuario,
        "estado_usuario": estado_usuario
    }

    try:
        dados = CriarUsuarioDTO(**dados_formulario, senha=senha, confirmar_senha=confirmar_senha)
        
        # if usuario_repo.obter_por_email(email):
        #     return templates.TemplateResponse(
        #         "publico/publico_cadastrar_doador.html",
        #         {"request": request, "erro": "Email já cadastrado"}
        #     )

        cidade = cidade_repo.obter_por_nome_estado(cidade_usuario, estado_usuario)
        if not cidade:
            cidade_id = cidade_repo.inserir(Cidade(cod_cidade=0, nome_cidade=cidade_usuario, sigla_estado=estado_usuario))
            print(f"Cidade inserida, id: {cidade_id}")
        else:
            cidade_id = cidade.cod_cidade
            print(f"Cidade já existe, id: {cidade_id}")

        senha_hash = criar_hash_senha(dados.senha)

        usuario = Usuario(
            cod_usuario=0,
            nome=dados.nome,
            email=dados.email,
            senha=senha_hash,
            cpf=dados.cpf,
            data_nascimento=dados.data_nascimento,
            status=1,
            rua_usuario=dados.rua_usuario,
            bairro_usuario=dados.bairro_usuario,
            cidade_usuario=cidade_id,
            cep_usuario=dados.cep_usuario,
            telefone=dados.telefone,
            perfil="doador",
            data_cadastro=None,
            estado_usuario=dados.estado_usuario
        )
        print(f"Tentando inserir usuario: {usuario}")
        try:
            usuario_id = usuario_repo.inserir(usuario)
            print(f"Usuário inserido, id: {usuario_id}")

            informar_sucesso(request, f"Cadastro realizado com sucesso! Bem-vindo(a), {dados.nome}!")
            return RedirectResponse("/validar_telefone", status.HTTP_303_SEE_OTHER)
        except sqlite3.IntegrityError as ie:
            # Tratamento comum: e-mail já existe (constraint UNIQUE)
            msg = str(ie)
            import traceback
            traceback.print_exc()
            if 'UNIQUE constraint failed' in msg and 'usuario.email' in msg:
                informar_erro(request, 'Email já cadastrado')
                return templates.TemplateResponse("publico/publico_cadastrar_doador.html", {
                    "request": request,
                    "erro": 'Email já cadastrado',
                    "erros": {},
                    "dados": dados_formulario
                })
            else:
                # outro erro de integridade
                informar_erro(request, 'Erro ao salvar usuário. Tente novamente.')
                return templates.TemplateResponse("publico/publico_cadastrar_doador.html", {
                    "request": request,
                    "erro": f"Erro ao salvar usuário: {msg}",
                    "erros": {},
                    "dados": dados_formulario
                })
    
    except ValidationError as e:
        # Mapear erros para cada campo usando os loc retornados pelo Pydantic
        erros_por_campo: dict = {}
        for erro in e.errors():
            loc = erro.get('loc') or []
            campo = loc[0] if loc else 'campo'
            mensagem = erro.get('msg', '')
            if isinstance(mensagem, str) and mensagem.startswith("Value error, "):
                mensagem = mensagem.replace("Value error, ", "")
            # Agrupa múltiplas mensagens por campo
            erros_por_campo.setdefault(campo, []).append(mensagem)

        # Construir mensagem resumida para flash
        resumo_erros = [f"{campo}: {', '.join(msgs)}" for campo, msgs in erros_por_campo.items()]
        erro_msg = " | ".join(resumo_erros)

        # Registrar/mostrar erro e retornar template com dados preservados e erros por campo
        informar_erro(request, "Há erros no formulário.")
        # Transformar listas em strings para facilitar uso no template
        erros_por_campo = {k: ' '.join(v) for k, v in erros_por_campo.items()}
        return templates.TemplateResponse("publico/publico_cadastrar_doador.html", {
            "request": request,
            "erro": erro_msg,
            "erros": erros_por_campo,
            "dados": dados_formulario  # Preservar dados digitados
        })

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        # Log completo no servidor (ajuda a debugar em dev)
        print("Erro ao processar cadastro:")
        print(tb)
        # Retornar mensagem com detalhe mínimo para desenvolvimento
        detalhado = str(e)
        informar_erro(request, "Erro ao processar cadastro. Tente novamente.")
        return templates.TemplateResponse("publico/publico_cadastrar_doador.html", {
            "request": request,
            "erro": f"Erro ao processar cadastro: {detalhado}",
            "erros": {},
            "dados": dados_formulario
        })

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
        {"request": request, "usuario": usuario_logado}
    )

# Rota apenas para administradores de unidade
@router.get("/administrador")
@requer_autenticacao(["administrador"])
async def get_administrador_dashboard(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse(
        "administrador_inicio.html",
        {"request": request, "usuario": usuario_logado}
    )

# Rota apenas para colaboradores
@router.get("/colaborador")
@requer_autenticacao(["colaborador"])
async def get_colaborador_dashboard(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse(
        "colaborador_inicio.html",
        {"request": request, "usuario": usuario_logado}
    )

# # Rota para múltiplos perfis
# @router.get("/relatorios")
# @requer_autenticacao(["admin", "gerente"])
# async def get_relatorios(request: Request, usuario_logado: dict = None):
#     return templates.TemplateResponse(
#         "relatorios.html",
#         {"request": request}
#     )