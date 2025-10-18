from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from data.repo import campanha_repo
from datetime import date

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/campanha/detalhes/{cod_campanha}")
async def get_colaborador_campanha_detalhe(request: Request, cod_campanha: int):
    # Buscar campanha específica do banco de dados
    campanha = campanha_repo.obter_por_id(cod_campanha)
    
    if not campanha:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    
    # Buscar campanhas relacionadas (outras campanhas ativas)
    todas_campanhas = campanha_repo.obter_todos()
    campanhas_relacionadas = [c for c in todas_campanhas if c.cod_campanha != cod_campanha and c.status == 1][:3]
    
    response = templates.TemplateResponse("colaborador/colaborador_campanha_detalhes.html", {
        "request": request, 
        "active_page": "campanha",
        "campanha": campanha,
        "campanhas_relacionadas": campanhas_relacionadas,
        "hoje": date.today()
    })
    return response
