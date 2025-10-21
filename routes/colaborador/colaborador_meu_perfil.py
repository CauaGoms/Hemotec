import os
from fastapi import APIRouter, File, Request, UploadFile, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from data.repo import cidade_repo, doador_repo, prontuario_repo, usuario_repo
from util.auth_decorator import requer_autenticacao
from util.doacao_utils import calcular_intervalo_doacao, obter_ultima_doacao_doador

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/meu_perfil")
@requer_autenticacao()
async def get_colaborador_meu_perfil(request: Request, usuario_logado: dict = None):
    usuario = usuario_repo.obter_por_id(usuario_logado['cod_usuario'])
    cidade = cidade_repo.obter_por_id(usuario_logado['cidade_usuario'])
    doador = doador_repo.obter_por_id(usuario_logado['cod_usuario'])
    
    # Calcular intervalo de doação
    ultima_doacao = obter_ultima_doacao_doador(usuario_logado['cod_usuario'])
    intervalo_doacao = calcular_intervalo_doacao(usuario.genero, ultima_doacao)
    
    # Buscar prontuário mais recente do doador
    prontuario = prontuario_repo.obter_por_doador(usuario_logado['cod_usuario'])
    
    response = templates.TemplateResponse("colaborador/colaborador_meu_perfil.html", {
        "request": request, 
        "active_page": "perfil", 
        "usuario": usuario, 
        "cidade": cidade, 
        "doador": doador,
        "intervalo_doacao": intervalo_doacao,
        "prontuario": prontuario
    })
    return response

@router.post("/colaborador/meu_perfil/alterar-foto")
@requer_autenticacao()
async def alterar_foto_colaborador(
    request: Request,
    foto: UploadFile = File(...),  # ← Recebe arquivo de foto
    usuario_logado: dict = None
):
    
    # 1. Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/colaborador/meu_perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)

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
        return RedirectResponse("/colaborador/meu_perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)

    return RedirectResponse("/colaborador/meu_perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)
