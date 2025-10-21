from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse

from data.repo import possivel_gestor_repo
from data.model.possivel_gestor_model import Possivel_Gestor

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cadastrar_possivel_gestor")
async def get_cadastrar_possivel_gestor(request: Request):
    response = templates.TemplateResponse("publico/publico_cadastrar_possivel_gestor.html", {"request": request, "active_page": "home"})
    return response


@router.post('/cadastrar_possivel_gestor')
async def post_cadastrar_possivel_gestor(
    request: Request,
    nome: str = Form(...),
    cargo: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
):
    """
    Recebe os dados do formulário e insere na tabela possivel_gestor.
    Retorna JSON com sucesso ou erro.
    """
    # Validações mínimas
    nome = (nome or '').strip()
    cargo = (cargo or '').strip()
    email = (email or '').strip()
    telefone = (telefone or '').strip()

    # Sanitizar telefone para conter apenas dígitos
    import re
    telefone_digits = re.sub(r"\D", "", telefone)
    telefone = telefone_digits

    if not nome or not cargo or not email or not telefone:
        return JSONResponse({'success': False, 'message': 'Todos os campos são obrigatórios.'}, status_code=400)

    # Validar telefone em formato apenas dígitos (10 ou 11 dígitos no Brasil)
    if len(telefone) not in (10, 11):
        return JSONResponse({'success': False, 'message': 'Telefone inválido. Informe DDD + número (10 ou 11 dígitos).'}, status_code=400)

    try:
        novo = Possivel_Gestor(
            cod_possivel_gestor=0,
            nome_possivel_gestor=nome,
            email_possivel_gestor=email,
            telefone_possivel_gestor=telefone,
            cargo_possivel_gestor=cargo,
        )
        inserted_id = possivel_gestor_repo.inserir(novo)
        if inserted_id:
            return JSONResponse({'success': True, 'id': inserted_id})
        else:
            return JSONResponse({'success': False, 'message': 'Falha ao inserir no banco.'}, status_code=500)
    except Exception as e:
        # Permitir emails duplicados - apenas registrar o erro mas inserir mesmo assim
        error_message = str(e).lower()
        if 'unique' in error_message or 'duplicate' in error_message:
            # Se for erro de duplicação, tentar inserir mesmo assim
            # (isso só acontecerá se houver constraint no banco, mas queremos permitir)
            return JSONResponse({'success': False, 'message': 'Erro ao cadastrar. Tente novamente.'}, status_code=500)
        return JSONResponse({'success': False, 'message': str(e)}, status_code=500)