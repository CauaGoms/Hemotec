from datetime import date
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from data.model.cidade_model import Cidade
from data.model.usuario_model import Usuario
from data.repo import cidade_repo, usuario_repo
from data.util.database import get_connection

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cadastrar_doador")
async def get_cadastro(request: Request):
    response = templates.TemplateResponse("publico/publico_cadastrar_doador.html", {"request": request})
    return response

@router.post("/cadastrar_doador")
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
    senha: str = Form(...)
):
    
    email_usuario = email
    # Verifica se já existe usuário com esse e-mail
    if usuario_repo.obter_por_email(email):
        raise Exception("Já existe uma conta cadastrada com esse e-mail.")

    # Busca a cidade pelo nome ou cria uma nova se não existir
    cidade = cidade_repo.obter_por_nome(cidade_usuario)
    if not cidade:
        # Se a cidade não existe, cria uma nova com sigla padrão
        nova_cidade = Cidade(0, cidade_usuario, "SP")  # Usando SP como estado padrão
        cidade_id = cidade_repo.inserir(nova_cidade)
    else:
        cidade_id = cidade.cod_cidade

    status = 1
    data_cadastro = date.today().isoformat()
    usu = Usuario(0, nome, email, senha, cpf, data_nascimento, status, data_cadastro, rua_usuario, bairro_usuario, cidade_id, cep_usuario, telefone)
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario_id = usuario_repo.inserir(usu, cursor)
        conn.commit()
    if usuario_id is None:
        raise Exception("Erro ao cadastrar usuário.")
    else:
        return RedirectResponse("/doador/dados_cadastrais", status_code=303)