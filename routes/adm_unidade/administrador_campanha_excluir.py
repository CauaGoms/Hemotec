from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/campanha/excluir/{cod_campanha}")
async def get_administrador_campanha_excluir(request: Request, cod_campanha: int):
    """Exibe página de confirmação de exclusão"""
    # Buscar campanha específica do banco de dados
    campanha = campanha_repo.obter_por_id(cod_campanha)
    
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    
    response = templates.TemplateResponse("adm_unidade/administrador_campanha_excluir.html", {
        "request": request, 
        "active_page": "campanha",
        "campanha": campanha
    })
    return response

@router.post("/administrador/campanha/excluir/{cod_campanha}/confirmar")
async def post_administrador_campanha_excluir_confirmar(request: Request, cod_campanha: int):
    """Executa a exclusão da campanha"""
    try:
        # Verificar se a campanha existe
        campanha = campanha_repo.obter_por_id(cod_campanha)
        
        if not campanha:
            raise HTTPException(status_code=404, detail="Campanha não encontrada")
        
        # Excluir campanha
        sucesso = campanha_repo.delete(cod_campanha)
        
        if sucesso:
            # Redirecionar para a lista de campanhas com mensagem de sucesso
            return RedirectResponse(url="/administrador/campanha", status_code=303)
        else:
            raise HTTPException(status_code=500, detail="Erro ao excluir campanha")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir campanha: {str(e)}")