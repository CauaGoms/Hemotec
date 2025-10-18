from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/campanha/editar/{cod_campanha}")
async def get_colaborador_campanha_alterar(request: Request, cod_campanha: int):
    """Exibe página de edição da campanha com os dados preenchidos"""
    # Buscar campanha específica do banco de dados
    campanha = campanha_repo.obter_por_id(cod_campanha)
    
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    
    response = templates.TemplateResponse("colaborador/colaborador_campanha_alterar.html", {
        "request": request, 
        "active_page": "campanha",
        "campanha": campanha
    })
    return response

@router.post("/colaborador/campanha/editar/{cod_campanha}")
async def post_colaborador_campanha_alterar(request: Request, cod_campanha: int):
    """Atualiza os dados da campanha"""
    try:
        # Verificar se a campanha existe
        campanha = campanha_repo.obter_por_id(cod_campanha)
        
        if not campanha:
            raise HTTPException(status_code=404, detail="Campanha não encontrada")
        
        # Aqui você implementaria a lógica de atualização
        # form_data = await request.form()
        # campanha_repo.update(cod_campanha, form_data)
        
        # Redirecionar para a lista de campanhas com mensagem de sucesso
        return RedirectResponse(url="/colaborador/campanha", status_code=303)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar campanha: {str(e)}")
