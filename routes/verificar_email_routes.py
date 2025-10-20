"""
Rotas para verificação de email
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data.repo import usuario_repo
from util.email_service import validar_codigo_verificacao, enviar_email_verificacao, gerar_codigo_verificacao
from util.flash_messages import informar_sucesso, informar_erro
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/verificar-email")
async def get_verificar_email(request: Request):
    """
    Exibe a tela de verificação de email.
    O email do usuário deve estar na sessão temporária.
    """
    # Obter email da sessão
    email = request.session.get("email_pendente_verificacao")
    nome = request.session.get("nome_pendente_verificacao", "")
    
    if not email:
        informar_erro(request, "Sessão expirada. Por favor, faça o cadastro novamente.")
        return RedirectResponse("/cadastrar", status_code=303)
    
    return templates.TemplateResponse("publico/publico_verificar_email.html", {
        "request": request,
        "email": email,
        "nome": nome
    })

@router.post("/verificar-email")
async def post_verificar_email(
    request: Request,
    codigo: str = Form(...)
):
    """
    Processa a verificação do código de email
    """
    # Obter email da sessão
    email = request.session.get("email_pendente_verificacao")
    nome = request.session.get("nome_pendente_verificacao", "")
    
    if not email:
        informar_erro(request, "Sessão expirada. Por favor, faça o cadastro novamente.")
        return RedirectResponse("/cadastrar", status_code=303)
    
    # Obter dados de verificação do usuário
    dados_verificacao = usuario_repo.obter_dados_verificacao(email)
    
    if not dados_verificacao:
        informar_erro(request, "Usuário não encontrado.")
        return templates.TemplateResponse("publico/publico_verificar_email.html", {
            "request": request,
            "email": email,
            "nome": nome,
            "erro": "Usuário não encontrado"
        })
    
    # Validar código
    codigo_valido = validar_codigo_verificacao(
        codigo_fornecido=codigo,
        codigo_armazenado=dados_verificacao["codigo_verificacao"],
        data_codigo=dados_verificacao["data_codigo_verificacao"],
        minutos_validade=30
    )
    
    if not codigo_valido:
        informar_erro(request, "Código inválido ou expirado. Verifique e tente novamente.")
        return templates.TemplateResponse("publico/publico_verificar_email.html", {
            "request": request,
            "email": email,
            "nome": nome,
            "erro": "Código inválido ou expirado"
        })
    
    # Marcar email como verificado
    sucesso = usuario_repo.marcar_email_verificado(email)
    
    if sucesso:
        # Limpar sessão temporária
        request.session.pop("email_pendente_verificacao", None)
        request.session.pop("nome_pendente_verificacao", None)
        
        informar_sucesso(request, "Email verificado com sucesso! Você já pode fazer login.")
        return RedirectResponse("/login", status_code=303)
    else:
        informar_erro(request, "Erro ao verificar email. Tente novamente.")
        return templates.TemplateResponse("publico/publico_verificar_email.html", {
            "request": request,
            "email": email,
            "nome": nome,
            "erro": "Erro ao processar verificação"
        })

@router.post("/reenviar-codigo-verificacao")
async def post_reenviar_codigo(request: Request):
    """
    Reenvia o código de verificação para o email do usuário
    """
    email = request.session.get("email_pendente_verificacao")
    nome = request.session.get("nome_pendente_verificacao", "")
    
    if not email:
        informar_erro(request, "Sessão expirada. Por favor, faça o cadastro novamente.")
        return RedirectResponse("/cadastrar", status_code=303)
    
    # Gerar novo código
    novo_codigo = gerar_codigo_verificacao()
    data_codigo = datetime.now().isoformat()
    
    # Atualizar código no banco
    sucesso_db = usuario_repo.atualizar_codigo_verificacao(email, novo_codigo, data_codigo)
    
    if not sucesso_db:
        informar_erro(request, "Erro ao gerar novo código. Tente novamente.")
        return RedirectResponse("/verificar-email", status_code=303)
    
    # Enviar email
    sucesso_email = enviar_email_verificacao(email, nome, novo_codigo)
    
    if sucesso_email:
        informar_sucesso(request, "Novo código enviado! Verifique sua caixa de entrada.")
    else:
        informar_erro(request, "Erro ao enviar email. Tente novamente em alguns instantes.")
    
    return RedirectResponse("/verificar-email", status_code=303)
