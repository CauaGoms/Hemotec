import os
from fastapi import APIRouter, File, Request, UploadFile, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from data.repo import usuario_repo
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dados_cadastrais")
async def get_doador_dados_cadastrais(request: Request):
    response = templates.TemplateResponse("usuario/dados_cadastrais.html", {"request": request, "active_page": "perfil"})
    return response

@router.post("/dados_cadastrais/alterar-foto")
@requer_autenticacao()
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),  # ← Recebe arquivo de foto
    usuario_logado: dict = None
):
    # 1. Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/dados_cadastrais?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)

    # 2. Criar diretório se não existir
    upload_dir = "static/uploads/usuarios"
    os.makedirs(upload_dir, exist_ok=True)

    # 3. Gerar nome único para evitar conflitos
    import secrets
    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{usuario_logado['cod_usuario']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

    # 4. Salvar arquivo no sistema
    try:
        conteudo = await foto.read()  # ← Lê conteúdo do arquivo
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        # 5. Salvar caminho no banco de dados
        caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"
        usuario_repo.atualizar_foto(usuario_logado['cod_usuario'], caminho_relativo)

        # 6. Atualizar sessão do usuário
        usuario_logado['foto'] = caminho_relativo
        from util.auth_decorator import criar_sessao
        criar_sessao(request, usuario_logado)

    except Exception as e:
        return RedirectResponse("/dados_cadastrais?erro=upload_falhou", status.HTTP_303_SEE_OTHER)

    return RedirectResponse("/dados_cadastrais?foto_sucesso=1", status.HTTP_303_SEE_OTHER)