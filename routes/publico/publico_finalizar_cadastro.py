from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from datetime import datetime
from pydantic_core import ValidationError
import re
import sqlite3

from data.repo import possivel_gestor_repo, instituicao_repo, usuario_repo, cidade_repo
from data.model.instituicao_model import Instituicao
from data.model.usuario_model import Usuario
from data.model.gestor_model import Gestor
from data.model.cidade_model import Cidade
from util.security import criar_hash_senha
from util.flash_messages import informar_sucesso, informar_erro
from dtos.gestor_dtos import CriarGestorDTO

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/finalizar_cadastro")
async def get_finalizar_cadastro(request: Request, possivel_id: int | None = None):
    """
    Se for passado ?possivel_id=..., busca os dados do possível gestor e passa ao template
    para pré-preenchimento dos campos.
    """
    possivel_gestor = None
    try:
        if possivel_id:
            possivel_gestor = possivel_gestor_repo.obter_por_id(possivel_id)
    except Exception:
        possivel_gestor = None

    response = templates.TemplateResponse(
        "publico/publico_finalizar_cadastro.html",
        {"request": request, "active_page": "home", "possivel_gestor": possivel_gestor},
    )
    return response


@router.post("/finalizar_cadastro")
async def post_finalizar_cadastro(
    request: Request,
    # Dados pessoais do gestor
    nome_gestor: str = Form(...),
    cpf_gestor: str = Form(...),
    email_gestor: str = Form(...),
    telefone_gestor: str = Form(...),
    data_nascimento_gestor: str = Form(...),
    genero_gestor: str = Form(...),
    # Endereço do gestor
    cep_gestor: str = Form(...),
    rua_gestor: str = Form(...),
    bairro_gestor: str = Form(...),
    cidade_gestor: str = Form(...),
    estado_gestor: str = Form(...),
    # Dados da instituição
    razao_social: str = Form(...),
    cnpj_instituicao: str = Form(...),
    email_institucional: str = Form(...),
    telefone_instituicao: str = Form(...),
    # Endereço da instituição
    cep_instituicao: str = Form(...),
    rua_instituicao: str = Form(...),
    bairro_instituicao: str = Form(...),
    cidade_instituicao: str = Form(...),
    estado_instituicao: str = Form(...),
    # Senha
    senha: str = Form(...),
):
    """
    Processa o formulário completo de cadastro:
    1. Valida todos os dados usando DTO
    2. Cria a Instituição
    3. Cria o Usuário (gestor)
    4. Cria o registro de Gestor vinculado à instituição
    """
    # Preservar dados do formulário para reexibição em caso de erro
    dados_formulario = {
        "nome_gestor": nome_gestor,
        "cpf_gestor": cpf_gestor,
        "email_gestor": email_gestor,
        "telefone_gestor": telefone_gestor,
        "data_nascimento_gestor": data_nascimento_gestor,
        "genero_gestor": genero_gestor,
        "cep_gestor": cep_gestor,
        "rua_gestor": rua_gestor,
        "bairro_gestor": bairro_gestor,
        "cidade_gestor": cidade_gestor,
        "estado_gestor": estado_gestor,
        "razao_social": razao_social,
        "cnpj_instituicao": cnpj_instituicao,
        "email_institucional": email_institucional,
        "telefone_instituicao": telefone_instituicao,
        "cep_instituicao": cep_instituicao,
        "rua_instituicao": rua_instituicao,
        "bairro_instituicao": bairro_instituicao,
        "cidade_instituicao": cidade_instituicao,
        "estado_instituicao": estado_instituicao,
    }

    try:
        # Validar dados usando DTO
        dados = CriarGestorDTO(**dados_formulario, senha=senha)
        # Buscar código da cidade do gestor
        cidade_gestor_obj = cidade_repo.obter_por_nome_estado(
            dados.cidade_gestor, dados.estado_gestor
        )
        if not cidade_gestor_obj:
            nova_cidade_gestor = Cidade(
                cod_cidade=0,
                nome_cidade=dados.cidade_gestor,
                sigla_estado=dados.estado_gestor
            )
            cod_cidade_gestor = cidade_repo.inserir(nova_cidade_gestor)
        else:
            cod_cidade_gestor = cidade_gestor_obj.cod_cidade

        # Buscar código da cidade da instituição
        cidade_inst_obj = cidade_repo.obter_por_nome_estado(
            dados.cidade_instituicao, dados.estado_instituicao
        )
        if not cidade_inst_obj:
            nova_cidade_inst = Cidade(
                cod_cidade=0,
                nome_cidade=dados.cidade_instituicao,
                sigla_estado=dados.estado_instituicao
            )
            cod_cidade_instituicao = cidade_repo.inserir(nova_cidade_inst)
        else:
            cod_cidade_instituicao = cidade_inst_obj.cod_cidade

        # 1. Criar Instituição
        instituicao = Instituicao(
            cod_instituicao=0,
            cnpj=dados.cnpj_instituicao,
            nome=dados.razao_social,
            email=dados.email_institucional,
            rua_instituicao=dados.rua_instituicao,
            bairro_instituicao=dados.bairro_instituicao,
            cidade_instituicao=cod_cidade_instituicao,
            cep_instituicao=dados.cep_instituicao,
            telefone=dados.telefone_instituicao
        )
        cod_instituicao = instituicao_repo.inserir(instituicao)

        if not cod_instituicao:
            informar_erro(request, "Erro ao criar instituição.")
            return templates.TemplateResponse(
                "publico/publico_finalizar_cadastro.html",
                {
                    "request": request,
                    "erro": "Erro ao criar instituição.",
                    "erros": {},
                    "dados": dados_formulario
                }
            )

        # 2. Criar Usuario (gestor)
        senha_hash = criar_hash_senha(dados.senha)
        data_nasc = datetime.strptime(dados.data_nascimento_gestor, "%Y-%m-%d").date()
        
        usuario = Usuario(
            cod_usuario=0,
            nome=dados.nome_gestor,
            email=dados.email_gestor,
            senha=senha_hash,
            cpf=dados.cpf_gestor,
            data_nascimento=data_nasc,
            status=True,
            rua_usuario=dados.rua_gestor,
            bairro_usuario=dados.bairro_gestor,
            cidade_usuario=cod_cidade_gestor,
            cep_usuario=dados.cep_gestor,
            telefone=dados.telefone_gestor,
            genero=dados.genero_gestor,
            perfil='gestor',
            data_cadastro=datetime.now().strftime("%Y-%m-%d"),
            foto=None,
            token_redefinicao=None,
            data_token=None,
            estado_usuario=dados.estado_gestor
        )
        
        cod_usuario = usuario_repo.inserir(usuario)

        if not cod_usuario:
            informar_erro(request, "Erro ao criar usuário.")
            return templates.TemplateResponse(
                "publico/publico_finalizar_cadastro.html",
                {
                    "request": request,
                    "erro": "Erro ao criar usuário.",
                    "erros": {},
                    "dados": dados_formulario
                }
            )

        # 3. Criar Gestor
        from util.database import get_connection
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gestor (cod_gestor, cod_instituicao, instituicao) VALUES (?, ?, ?)",
                (cod_usuario, cod_instituicao, dados.razao_social)
            )
            conn.commit()

        # Redirecionar para login com mensagem de sucesso
        informar_sucesso(request, "Cadastro realizado com sucesso! Faça login para continuar.")
        return RedirectResponse(url="/login", status_code=303)

    except ValidationError as e:
        # Mapear erros para cada campo
        erros_por_campo: dict = {}
        for erro in e.errors():
            loc = erro.get('loc') or []
            campo = loc[0] if loc else 'campo'
            mensagem = erro.get('msg', '')
            if isinstance(mensagem, str) and mensagem.startswith("Value error, "):
                mensagem = mensagem.replace("Value error, ", "")
            erros_por_campo.setdefault(campo, []).append(mensagem)

        # Construir mensagem resumida
        resumo_erros = [f"{campo}: {', '.join(msgs)}" for campo, msgs in erros_por_campo.items()]
        erro_msg = " | ".join(resumo_erros)

        informar_erro(request, "Há erros no formulário.")
        # Transformar listas em strings
        erros_por_campo = {k: ' '.join(v) for k, v in erros_por_campo.items()}
        
        return templates.TemplateResponse(
            "publico/publico_finalizar_cadastro.html",
            {
                "request": request,
                "erro": erro_msg,
                "erros": erros_por_campo,
                "dados": dados_formulario
            }
        )

    except sqlite3.IntegrityError as ie:
        msg = str(ie)
        import traceback
        traceback.print_exc()
        
        if 'UNIQUE constraint failed' in msg and 'usuario.email' in msg:
            informar_erro(request, 'Email já cadastrado')
            return templates.TemplateResponse(
                "publico/publico_finalizar_cadastro.html",
                {
                    "request": request,
                    "erro": 'Email já cadastrado',
                    "erros": {"email_gestor": "Este email já está cadastrado"},
                    "dados": dados_formulario
                }
            )
        else:
            informar_erro(request, 'Erro ao salvar no banco de dados.')
            return templates.TemplateResponse(
                "publico/publico_finalizar_cadastro.html",
                {
                    "request": request,
                    "erro": f"Erro ao salvar: {msg}",
                    "erros": {},
                    "dados": dados_formulario
                }
            )

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print("Erro ao finalizar cadastro:")
        print(tb)
        
        informar_erro(request, "Erro ao processar cadastro. Tente novamente.")
        return templates.TemplateResponse(
            "publico/publico_finalizar_cadastro.html",
            {
                "request": request,
                "erro": f"Erro ao processar cadastro: {str(e)}",
                "erros": {},
                "dados": dados_formulario
            }
        )