from datetime import date
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from data.model.doador_model import Doador
from data.model.prontuario_model import Prontuario
from data.repo import doador_repo, prontuario_repo, usuario_repo
from data.util.database import get_connection

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/doacao/adicionar")
async def get_colaborador_doacao_adicionar(request: Request):
    response = templates.TemplateResponse("colaborador/colaborador_doacao_adicionar.html", {"request": request, "active_page": "doacao"})
    return response

@router.post("/colaborador/doacao/adicionar")
async def post_colaborador_doacao_adicionar(
    request: Request,
    altura: float = Form(...),
    peso: int = Form(...),
    tipo_sanguineo: str = Form(...),
    profissao: str = Form(...),
    contato_emergencia: str = Form(...),
    telefone_emergencia: str = Form(...),
    diabetes: bool = Form(False),
    hipertensao: bool = Form(False),
    cardiopatia: bool = Form(False),
    cancer: bool = Form(False),
    nenhuma: bool = Form(False),
    outros: bool = Form(False),
    medicamentos: str = Form("Nenhum"),
    fumante: str = Form("Não"),
    alcool: str = Form("Não"),
    atividade_fisica: str = Form("Não"),
    jejum: str = Form(False),
    sono: str = Form(False),
    bebida: str = Form(False),
    sintomas_gripais: str = Form(False),
    tatuagem: str = Form(False),
    termos: str = Form(False),
    alerta: str = Form(False)
):
    # 1. Obtenha o identificador do usuário logado a partir da sessão
    email_usuario = request.session.get("user_email")
    if not email_usuario:
        raise Exception("Usuário não está logado.")

    # 2. Busque o usuário no banco
    usuario = usuario_repo.obter_por_email(email_usuario)
    if not usuario:
        raise Exception("Usuário não encontrado.")

    data_atualizacao = date.today().isoformat()
    prontuario = Prontuario(
        0, 0, data_atualizacao, data_atualizacao, diabetes, hipertensao, cardiopatia, cancer, nenhuma, outros,
        medicamentos, fumante, alcool, atividade_fisica, jejum, sono, bebida, sintomas_gripais, tatuagem, termos, alerta
    )

    elegivel = True  # Defina a elegibilidade como True por padrão

    # extraindo o fator Rh do tipo sanguíneo
    fator_rh = ""
    if tipo_sanguineo.endswith("+"):
        fator_rh = "+"
    elif tipo_sanguineo.endswith("-"):
        fator_rh = "-"

    # 3. Crie o doador usando os dados do usuário buscado
    doador = Doador(
        0, 0, 0, tipo_sanguineo, fator_rh, elegivel, altura, peso, profissao, contato_emergencia, telefone_emergencia
    )

    with get_connection() as conn:
        cursor = conn.cursor()
        prontuario_id = prontuario_repo.inserir(prontuario, cursor)
        doador_id = doador_repo.inserir(doador, cursor)
        conn.commit()
    if prontuario_id is None or doador_id is None:
        raise Exception("Erro ao cadastrar prontuario ou doador.")
    else:
        return RedirectResponse("/doador", status_code=303)