from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.repo import usuario_repo
from util.security import gerar_token_redefinicao, obter_data_expiracao_token, criar_hash_senha, validar_token_expiracao
from util.email_service import email_service

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/redefinir_senha")
async def get_redefinir_senha(request: Request):
    """Exibe formulário para solicitar recuperação de senha"""
    response = templates.TemplateResponse("publico/publico_redefinir_senha.html", {"request": request})
    return response


@router.post("/redefinir_senha")
async def post_redefinir_senha(request: Request, email: str = Form(...)):
    """
    Processa solicitação de recuperação de senha:
    1. Verifica se email existe
    2. Gera token único
    3. Salva token no banco com data de expiração
    4. Envia email com link de recuperação
    """
    try:
        # Busca usuário por email
        usuario = usuario_repo.obter_por_email(email)
        
        if not usuario:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "E-mail não encontrado no sistema."}
            )
        
        # Gera token de recuperação (válido por 1 hora)
        token = gerar_token_redefinicao()
        data_expiracao = obter_data_expiracao_token(horas=1)
        
        # DEBUG: Mostra token no console (remover em produção)
        print(f"\n{'='*60}")
        print(f"🔑 TOKEN DE RECUPERAÇÃO GERADO")
        print(f"{'='*60}")
        print(f"Email: {email}")
        print(f"Token: {token}")
        print(f"Link: http://localhost:8000/redefinir-senha?token={token}")
        print(f"Expira em: {data_expiracao}")
        print(f"{'='*60}\n")
        
        # Salva token no banco
        sucesso = usuario_repo.atualizar_token(email, token, data_expiracao)
        
        if not sucesso:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Erro ao processar solicitação."}
            )
        
        # Envia email com link de recuperação
        email_enviado = email_service.enviar_recuperacao_senha(
            para_email=email,
            para_nome=usuario.nome,
            token=token
        )
        
        if not email_enviado:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Erro ao enviar e-mail. Tente novamente."}
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True, 
                "message": "E-mail de recuperação enviado com sucesso! Verifique sua caixa de entrada."
            }
        )
        
    except Exception as e:
        print(f"Erro ao processar recuperação de senha: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Erro interno. Tente novamente mais tarde."}
        )


@router.get("/redefinir-senha")
async def get_redefinir_senha_com_token(request: Request, token: str = None):
    """
    Valida token recebido via query string e exibe formulário para nova senha
    """
    if not token:
        return RedirectResponse(url="/redefinir_senha", status_code=303)
    
    # Busca usuário por token
    usuario = usuario_repo.obter_por_token(token)
    
    if not usuario:
        return templates.TemplateResponse(
            "publico/publico_redefinir_senha.html",
            {
                "request": request,
                "erro": "Token inválido ou expirado. Solicite um novo link de recuperação."
            }
        )
    
    # Verifica se token está expirado
    if not validar_token_expiracao(usuario.data_token):
        # Limpa token expirado
        usuario_repo.limpar_token(usuario.cod_usuario)
        return templates.TemplateResponse(
            "publico/publico_redefinir_senha.html",
            {
                "request": request,
                "erro": "Token expirado. Solicite um novo link de recuperação."
            }
        )
    
    # Token válido - exibe formulário de nova senha
    return templates.TemplateResponse(
        "publico/publico_criar_nova_senha.html",
        {
            "request": request,
            "token": token,
            "email": usuario.email
        }
    )


@router.post("/redefinir-senha")
async def post_redefinir_senha_nova(
    request: Request,
    token: str = Form(...),
    nova_senha: str = Form(...),
    confirmar_senha: str = Form(...)
):
    """
    Processa a redefinição de senha:
    1. Valida token
    2. Valida senhas (match e requisitos mínimos)
    3. Atualiza senha no banco
    4. Limpa token
    """
    try:
        # Valida se senhas conferem
        if nova_senha != confirmar_senha:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "As senhas não conferem."}
            )
        
        # Valida requisitos mínimos da senha
        if len(nova_senha) < 6:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "A senha deve ter pelo menos 6 caracteres."}
            )
        
        # Busca usuário por token
        usuario = usuario_repo.obter_por_token(token)
        
        if not usuario:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Token inválido."}
            )
        
        # Verifica se token está expirado
        if not validar_token_expiracao(usuario.data_token):
            usuario_repo.limpar_token(usuario.cod_usuario)
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Token expirado. Solicite um novo link."}
            )
        
        # Cria hash da nova senha
        senha_hash = criar_hash_senha(nova_senha)
        
        # Atualiza senha no banco
        sucesso = usuario_repo.atualizar_senha(usuario.cod_usuario, senha_hash)
        
        if not sucesso:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Erro ao atualizar senha."}
            )
        
        # Limpa token após uso
        usuario_repo.limpar_token(usuario.cod_usuario)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Senha redefinida com sucesso! Você já pode fazer login."
            }
        )
        
    except Exception as e:
        print(f"Erro ao redefinir senha: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Erro interno. Tente novamente."}
        )