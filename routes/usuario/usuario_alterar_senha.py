from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from data.repo import usuario_repo
from util.auth_decorator import requer_autenticacao
from util.security import criar_hash_senha

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/usuario/alterar_senha")
@requer_autenticacao()
async def get_usuario_alterar_senha(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("usuario/usuario_alterar_senha.html", {
        "request": request, 
        "active_page": "alterar_senha",
        "usuario": usuario_logado
    })
    return response

@router.post("/usuario/alterar_senha")
@requer_autenticacao()
async def post_usuario_alterar_senha(
    request: Request,
    nova_senha: str = Form(...),
    confirmar_senha: str = Form(...),
    usuario_logado: dict = None
):
    try:
        # Buscar usuário completo do banco
        usuario_db = usuario_repo.obter_por_id(usuario_logado["cod_usuario"])
        
        if not usuario_db:
            return templates.TemplateResponse(
                "usuario/usuario_alterar_senha.html",
                {
                    "request": request,
                    "usuario": usuario_logado,
                    "active_page": "alterar_senha",
                    "erro": "Usuário não encontrado."
                }
            )
        
        # Verificar se as senhas conferem
        if nova_senha != confirmar_senha:
            return templates.TemplateResponse(
                "usuario/usuario_alterar_senha.html",
                {
                    "request": request,
                    "usuario": usuario_logado,
                    "active_page": "alterar_senha",
                    "erro": "A nova senha e a confirmação não conferem."
                }
            )
        
        # Verificar se a nova senha tem pelo menos 6 caracteres
        if len(nova_senha) < 6:
            return templates.TemplateResponse(
                "usuario/usuario_alterar_senha.html",
                {
                    "request": request,
                    "usuario": usuario_logado,
                    "active_page": "alterar_senha",
                    "erro": "A nova senha deve ter pelo menos 6 caracteres."
                }
            )
        
        # Hash da nova senha
        senha_hash = criar_hash_senha(nova_senha)
        
        # Atualizar senha no banco
        sucesso = usuario_repo.atualizar_senha(usuario_db.cod_usuario, senha_hash)
        
        if sucesso:
            return templates.TemplateResponse(
                "usuario/usuario_alterar_senha.html",
                {
                    "request": request,
                    "usuario": usuario_logado,
                    "active_page": "alterar_senha",
                    "sucesso": "Senha alterada com sucesso!"
                }
            )
        else:
            return templates.TemplateResponse(
                "usuario/usuario_alterar_senha.html",
                {
                    "request": request,
                    "usuario": usuario_logado,
                    "active_page": "alterar_senha",
                    "erro": "Erro ao alterar senha. Tente novamente."
                }
            )
    except Exception as e:
        print(f"Erro ao alterar senha: {e}")
        return templates.TemplateResponse(
            "usuario/usuario_alterar_senha.html",
            {
                "request": request,
                "usuario": usuario_logado,
                "active_page": "alterar_senha",
                "erro": f"Erro ao processar alteração: {str(e)}"
            }
        )
