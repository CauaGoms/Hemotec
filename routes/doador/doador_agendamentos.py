import datetime
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import agendamento_repo, unidade_coleta_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/agendamento")
async def get_doador_agendamento(request: Request):
    agendamentos_concluidos = []
    agendamentos_agendados = []
    agendamentos_atrasados = []
    agendamentos = agendamento_repo.obter_todos()
    for agendamento in agendamentos:
        id_local_agendamento = agendamento.local_agendamento
        local_agendamento = unidade_coleta_repo.obter_por_id(id_local_agendamento)
        if agendamento.status == 1:
            agendamentos_concluidos.append([agendamento, local_agendamento])
        elif agendamento.status == 0:
            if agendamento.data_hora < datetime.datetime.now():
                agendamentos_atrasados.append([agendamento, local_agendamento])
            else:
                agendamentos_agendados.append([agendamento, local_agendamento])

    

    response = templates.TemplateResponse("doador/doador_agendamento.html", {"request": request, "active_page": "agendamento", "agendamentos_concluidos": agendamentos_concluidos, "agendamentos_agendados": agendamentos_agendados, "agendamentos_atrasados": agendamentos_atrasados})
    return response