import datetime
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from data.repo import agendamento_repo, unidade_coleta_repo, doador_repo, doacao_repo, usuario_repo
from data.model.doacao_model import Doacao
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class ConfirmarPresencaRequest(BaseModel):
    cod_agendamento: int
    cod_doador: int

@router.get("/colaborador/agendamento")
@requer_autenticacao(["colaborador"])
async def get_colaborador_agendamento(request: Request, usuario_logado: dict = None):
    agendamentos_concluidos = []
    agendamentos_agendados = []
    agendamentos_atrasados = []
    agendamentos = agendamento_repo.obter_todos()
    
    for agendamento in agendamentos:
        id_local_agendamento = agendamento.local_agendamento
        local_agendamento = unidade_coleta_repo.obter_por_id(id_local_agendamento)
        doador = doador_repo.obter_por_id(agendamento.cod_doador) if agendamento.cod_doador else None
        usuario_doador = usuario_repo.obter_por_id(agendamento.cod_doador) if agendamento.cod_doador else None
        
        # Criar objeto combinado com dados do doador e usuário
        doador_completo = {
            'doador': doador,
            'usuario': usuario_doador
        }
        
        if agendamento.status == 1:
            agendamentos_concluidos.append([agendamento, local_agendamento, doador_completo])
        elif agendamento.status == 0:
            if agendamento.data_hora < datetime.datetime.now():
                agendamentos_atrasados.append([agendamento, local_agendamento, doador_completo])
            else:
                agendamentos_agendados.append([agendamento, local_agendamento, doador_completo])

    response = templates.TemplateResponse(
        "colaborador/colaborador_agendamento.html", 
        {
            "request": request, 
            "active_page": "agendamento",
            "usuario": usuario_logado,
            "agendamentos_concluidos": agendamentos_concluidos,
            "agendamentos_agendados": agendamentos_agendados,
            "agendamentos_atrasados": agendamentos_atrasados
        }
    )
    return response

@router.post("/api/colaborador/agendamento/confirmar-presenca")
@requer_autenticacao(["colaborador"])
async def confirmar_presenca_agendamento(request: Request, dados: ConfirmarPresencaRequest, usuario_logado: dict = None):
    try:
        # Criar nova doação
        nova_doacao = Doacao(
            cod_doador=dados.cod_doador,
            cod_agendamento=dados.cod_agendamento,
            data_hora=datetime.datetime.now(),
            quantidade=None,  # Será preenchido posteriormente
            status=0,  # Status pendente
            observacoes="Doação criada automaticamente ao confirmar presença"
        )
        
        # Inserir doação no banco
        doacao_repo.inserir(nova_doacao)
        
        # Atualizar status do agendamento para concluído
        agendamento = agendamento_repo.obter_por_id(dados.cod_agendamento)
        if agendamento:
            agendamento.status = 1  # Concluído
            agendamento_repo.update(agendamento)
        
        return JSONResponse(content={
            "success": True,
            "message": "Presença confirmada e doação criada com sucesso!"
        })
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "message": str(e)
        }, status_code=500)
