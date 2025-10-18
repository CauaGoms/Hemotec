from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from data.repo import agendamento_repo, unidade_coleta_repo, doador_repo, usuario_repo
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/agendamento/excluir/{id_agendamento}")
@requer_autenticacao(["colaborador"])
async def get_colaborador_agendamento_excluir(request: Request, id_agendamento: int, usuario_logado: dict = None):
    agendamento = agendamento_repo.obter_por_id(id_agendamento)
    unidade = None
    doador_completo = None
    
    if agendamento:
        if agendamento.local_agendamento:
            unidade = unidade_coleta_repo.obter_por_id(agendamento.local_agendamento)
        if agendamento.cod_doador:
            doador = doador_repo.obter_por_id(agendamento.cod_doador)
            usuario_doador = usuario_repo.obter_por_id(agendamento.cod_doador)
            doador_completo = {
                'doador': doador,
                'usuario': usuario_doador
            }
    
    # Converter agendamento para dict - passar como string simples
    agendamento_dict = None
    if agendamento:
        agendamento_dict = {
            'cod_agendamento': agendamento.cod_agendamento,
            'cod_colaborador': agendamento.cod_colaborador,
            'cod_doador': agendamento.cod_doador,
            'data_hora': str(agendamento.data_hora) if agendamento.data_hora else None,  # Simples: "2025-10-21 09:00:00"
            'status': agendamento.status,
            'tipo_agendamento': agendamento.tipo_agendamento,
            'local_agendamento': agendamento.local_agendamento
        }
    
    response = templates.TemplateResponse(
        "colaborador/colaborador_agendamento_excluir.html", 
        {
            "request": request, 
            "active_page": "agendamento",
            "usuario": usuario_logado,
            "agendamento": agendamento_dict,
            "unidade": unidade,
            "doador": doador_completo
        }
    )
    
    return response

@router.post("/colaborador/agendamento/excluir/{id_agendamento}/confirmar")
@requer_autenticacao(["colaborador"])
async def post_colaborador_agendamento_excluir_confirmar(request: Request, id_agendamento: int, usuario_logado: dict = None):
    sucesso = agendamento_repo.delete(id_agendamento)
    if sucesso:
        return RedirectResponse(url="/colaborador/agendamento", status_code=303)
    else:
        return templates.TemplateResponse(
            "colaborador/colaborador_agendamento_excluir.html",
            {
                "request": request,
                "active_page": "agendamento",
                "usuario": usuario_logado,
                "erro": "Não foi possível excluir o agendamento."
            }
        )
