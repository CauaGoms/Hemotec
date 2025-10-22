from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import campanha_repo
from data.model.campanha_model import Campanha
from datetime import datetime
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/campanha/adicionar")
@requer_autenticacao(["administrador"])
async def get_administrador_campanha_adicionar(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse(
        "adm_unidade/administrador_campanha_adicionar.html", 
        {
            "request": request, 
            "active_page": "campanha",
            "usuario": usuario_logado
        }
    )
    return response

@router.post("/api/administrador/campanha/adicionar")
@requer_autenticacao(["administrador"])
async def post_administrador_campanha_adicionar(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    data_inicio: str = Form(...),
    data_fim: str = Form(...),
    foto: UploadFile = File(None),
    usuario_logado: dict = None
):
    """Adiciona uma nova campanha ao banco de dados"""
    try:
        # Processar foto se fornecida
        foto_path = None
        if foto and foto.filename:
            # Criar diretório se não existir
            upload_dir = "static/uploads/campanhas"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Salvar arquivo
            file_path = os.path.join(upload_dir, foto.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(await foto.read())
            foto_path = f"/uploads/campanhas/{foto.filename}"
        
        # Criar objeto Campanha
        campanha = Campanha(
            cod_campanha=0,  # Será gerado pelo banco
            titulo=titulo,
            descricao=descricao,
            data_inicio=datetime.strptime(data_inicio, "%Y-%m-%d").date(),
            data_fim=datetime.strptime(data_fim, "%Y-%m-%d").date(),
            status="ativa",
            foto=foto_path
        )
        
        # Inserir campanha no banco
        cod_campanha = campanha_repo.inserir(campanha)
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Campanha criada com sucesso!",
                "cod_campanha": cod_campanha
            },
            status_code=201
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao criar campanha: {str(e)}"
            },
            status_code=500
        )