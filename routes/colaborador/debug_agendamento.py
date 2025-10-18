from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from data.repo import agendamento_repo
from util.auth_decorator import requer_autenticacao

router = APIRouter()

@router.get("/api/debug/agendamento/{id_agendamento}")
@requer_autenticacao(["colaborador"])
async def debug_agendamento(request: Request, id_agendamento: int, usuario_logado: dict = None):
    agendamento = agendamento_repo.obter_por_id(id_agendamento)
    
    if not agendamento:
        return JSONResponse(content={"error": "Agendamento não encontrado"}, status_code=404)
    
    return JSONResponse(content={
        "cod_agendamento": agendamento.cod_agendamento,
        "cod_doador": agendamento.cod_doador,
        "cod_colaborador": agendamento.cod_colaborador,
        "data_hora": str(agendamento.data_hora) if agendamento.data_hora else None,
        "data_hora_type": str(type(agendamento.data_hora)),
        "status": agendamento.status,
        "tipo_agendamento": agendamento.tipo_agendamento,
        "local_agendamento": agendamento.local_agendamento
    })
