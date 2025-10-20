from fastapi import APIRouter, Request, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import campanha_repo
from data.model.campanha_model import Campanha
from datetime import datetime
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/campanha/editar/{cod_campanha}")
@requer_autenticacao(["colaborador"])
async def get_colaborador_campanha_alterar(request: Request, cod_campanha: int, usuario_logado: dict = None):
    """Exibe página de edição da campanha com os dados preenchidos"""
    # Buscar campanha específica do banco de dados
    campanha = campanha_repo.obter_por_id(cod_campanha)
    
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    
    response = templates.TemplateResponse("colaborador/colaborador_campanha_alterar.html", {
        "request": request, 
        "active_page": "campanha",
        "campanha": campanha,
        "usuario": usuario_logado
    })
    return response

@router.post("/api/colaborador/campanha/editar/{cod_campanha}")
@requer_autenticacao(["colaborador"])
async def post_colaborador_campanha_alterar(
    request: Request,
    cod_campanha: int,
    titulo: str = Form(...),
    descricao: str = Form(...),
    data_inicio: str = Form(...),
    data_fim: str = Form(...),
    foto: UploadFile = File(None),
    usuario_logado: dict = None
):
    """Atualiza os dados da campanha"""
    try:
        # Verificar se a campanha existe
        campanha = campanha_repo.obter_por_id(cod_campanha)
        
        if not campanha:
            raise HTTPException(status_code=404, detail="Campanha não encontrada")
        
        # Processar foto se fornecida
        foto_path = campanha.foto  # Manter foto anterior
        if foto and foto.filename:
            # Criar diretório se não existir
            upload_dir = "static/uploads/campanhas"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Salvar arquivo
            file_path = os.path.join(upload_dir, foto.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(await foto.read())
            foto_path = f"/uploads/campanhas/{foto.filename}"
        
        # Atualizar objeto Campanha
        campanha_atualizada = Campanha(
            cod_campanha=cod_campanha,
            titulo=titulo,
            descricao=descricao,
            data_inicio=datetime.strptime(data_inicio, "%Y-%m-%d").date(),
            data_fim=datetime.strptime(data_fim, "%Y-%m-%d").date(),
            status=campanha.status,  # Manter status anterior
            foto=foto_path
        )
        
        # Atualizar no banco
        sucesso = campanha_repo.update(campanha_atualizada)
        
        if not sucesso:
            return JSONResponse(
                content={
                    "success": False,
                    "message": "Falha ao atualizar campanha"
                },
                status_code=500
            )
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Campanha atualizada com sucesso!",
                "cod_campanha": cod_campanha
            },
            status_code=200
        )
            
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao atualizar campanha: {str(e)}"
            },
            status_code=500
        )
