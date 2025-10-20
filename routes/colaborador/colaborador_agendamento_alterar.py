from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from data.repo import agendamento_repo, unidade_coleta_repo, doador_repo, usuario_repo
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class AlterarAgendamentoRequest(BaseModel):
    local_agendamento: int
    data_hora: str

@router.get("/colaborador/agendamento/alterar/{id_agendamento}")
@requer_autenticacao(["colaborador"])
async def get_colaborador_agendamento_alterar(request: Request, id_agendamento: int, usuario_logado: dict = None):
    agendamento = agendamento_repo.obter_por_id(id_agendamento)
    unidade = None
    doador_completo = None
    
    if agendamento:
        if agendamento.local_agendamento:
            unidade = unidade_coleta_repo.obter_por_id(agendamento.local_agendamento)
        if agendamento.cod_usuario:
            doador = doador_repo.obter_por_id(agendamento.cod_usuario)
            usuario_doador = usuario_repo.obter_por_id(agendamento.cod_usuario)
            doador_completo = {
                'doador': doador,
                'usuario': usuario_doador
            }
    
    unidades = unidade_coleta_repo.obter_todos()
    
    # Converter agendamento para dict - passar como string simples
    agendamento_dict = None
    if agendamento:
        agendamento_dict = {
            'cod_agendamento': agendamento.cod_agendamento,
            'cod_colaborador': agendamento.cod_colaborador,
            'cod_usuario': agendamento.cod_usuario,
            'data_hora': str(agendamento.data_hora) if agendamento.data_hora else None,  # Simples: "2025-10-21 09:00:00"
            'status': agendamento.status,
            'tipo_agendamento': agendamento.tipo_agendamento,
            'local_agendamento': agendamento.local_agendamento
        }
    
    response = templates.TemplateResponse(
        "colaborador/colaborador_agendamento_alterar.html", 
        {
            "request": request, 
            "active_page": "agendamento",
            "usuario": usuario_logado,
            "agendamento": agendamento_dict,
            "unidade": unidade,
            "doador": doador_completo,
            "unidades": unidades
        }
    )
    return response

@router.put("/api/colaborador/agendamento/alterar/{id_agendamento}")
@requer_autenticacao(["colaborador"])
async def alterar_agendamento(request: Request, id_agendamento: int, dados: AlterarAgendamentoRequest, usuario_logado: dict = None):
    try:
        # Buscar o agendamento
        agendamento = agendamento_repo.obter_por_id(id_agendamento)
        
        if not agendamento:
            return JSONResponse(content={
                "success": False,
                "message": "Agendamento não encontrado"
            }, status_code=404)
        
        # Atualizar os dados
        agendamento.local_agendamento = dados.local_agendamento
        agendamento.data_hora = datetime.fromisoformat(dados.data_hora)
        
        # Salvar no banco
        agendamento_repo.update(agendamento)
        
        return JSONResponse(content={
            "success": True,
            "message": "Agendamento alterado com sucesso!"
        })
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "message": str(e)
        }, status_code=500)
