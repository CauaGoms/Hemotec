from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/agendamento/historico_agendamentos")
async def get_doador_historico_agendamentos(request: Request):
    try:
        response = templates.TemplateResponse("doador/doador_historico_agendamento.html", {"request": request, "active_page": "agendamento"})
        return response
    except Exception as e:
        print(f"Erro ao carregar histórico de agendamentos: {e}")
        # Fallback para uma página simples se o template não for encontrado
        return {"message": "Página de histórico de agendamentos", "error": str(e)}