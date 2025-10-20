from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from util.auth_decorator import requer_autenticacao
from data.repo import agendamento_repo, agenda_repo, unidade_coleta_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/agendamento/excluir/{cod_agendamento}")
@requer_autenticacao(["doador"])
async def get_doador_agendamento_excluir(cod_agendamento: int, request: Request, usuario_logado: dict = None):
    """
    Exibe a tela de confirmação de exclusão do agendamento
    """
    # Busca o agendamento
    agendamento = agendamento_repo.obter_por_id(cod_agendamento)
    
    if not agendamento:
        return RedirectResponse(url="/doador/agendamento", status_code=302)
    
    # Verifica se o agendamento pertence ao usuário
    if agendamento.cod_usuario != usuario_logado.get('cod_usuario'):
        return RedirectResponse(url="/doador/agendamento", status_code=302)
    
    # Busca informações da unidade
    unidade = unidade_coleta_repo.obter_por_id(agendamento.local_agendamento)
    
    response = templates.TemplateResponse("doador/doador_agendamento_excluir.html", {
        "request": request, 
        "active_page": "agendamento",
        "usuario": usuario_logado,
        "agendamento": agendamento,
        "unidade": unidade
    })
    return response

@router.post("/doador/agendamento/excluir/{cod_agendamento}/confirmar")
@requer_autenticacao(["doador"])
async def confirmar_exclusao_agendamento(cod_agendamento: int, request: Request, usuario_logado: dict = None):
    """
    Processa a exclusão do agendamento após confirmação
    """
    try:
        # Verifica se o agendamento existe
        agendamento = agendamento_repo.obter_por_id(cod_agendamento)
        if not agendamento:
            return RedirectResponse(url="/doador/agendamento?erro=agendamento_nao_encontrado", status_code=302)
        
        # Verifica se o agendamento pertence ao usuário logado
        if agendamento.cod_usuario != usuario_logado.get('cod_usuario'):
            return RedirectResponse(url="/doador/agendamento?erro=sem_permissao", status_code=302)
        
        # Busca a agenda associada para decrementar quantidade_doadores
        from datetime import datetime
        
        # Busca a agenda pela data/hora e local
        agendas = agenda_repo.obter_por_unidade_e_data(
            agendamento.local_agendamento, 
            agendamento.data_hora.date()
        )
        
        # Encontra a agenda específica pelo horário
        agenda_encontrada = None
        for agenda in agendas:
            if agenda.hora_agenda == agendamento.data_hora.time():
                agenda_encontrada = agenda
                break
        
        # Exclui o agendamento
        sucesso = agendamento_repo.delete(cod_agendamento)
        
        if not sucesso:
            return RedirectResponse(url="/doador/agendamento?erro=falha_exclusao", status_code=302)
        
        # Decrementa a quantidade de doadores na agenda se encontrada
        if agenda_encontrada:
            agenda_repo.decrementar_doadores(agenda_encontrada.cod_agenda)
        
        return RedirectResponse(url="/doador/agendamento?sucesso=agendamento_excluido", status_code=302)
        
    except Exception as e:
        return RedirectResponse(url=f"/doador/agendamento?erro=erro_sistema", status_code=302)

@router.delete("/api/doador/agendamento/{cod_agendamento}")
@requer_autenticacao(["doador"])
async def excluir_agendamento(cod_agendamento: int, request: Request, usuario_logado: dict = None):
    """
    Exclui um agendamento e decrementa a quantidade de doadores na agenda.
    """
    try:
        # Verifica se o agendamento existe
        agendamento = agendamento_repo.obter_por_id(cod_agendamento)
        if not agendamento:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        # Verifica se o agendamento pertence ao usuário logado
        if agendamento.cod_usuario != usuario_logado.get('cod_usuario'):
            raise HTTPException(status_code=403, detail="Você não tem permissão para excluir este agendamento")
        
        # Busca a agenda associada para decrementar quantidade_doadores
        # Precisamos obter o cod_agenda a partir dos dados do agendamento
        from data.repo import agenda_repo
        from datetime import datetime
        
        # Busca a agenda pela data/hora e local
        agendas = agenda_repo.obter_por_unidade_e_data(
            agendamento.local_agendamento, 
            agendamento.data_hora.date()
        )
        
        # Encontra a agenda específica pelo horário
        agenda_encontrada = None
        for agenda in agendas:
            if agenda.hora_agenda == agendamento.data_hora.time():
                agenda_encontrada = agenda
                break
        
        # Exclui o agendamento
        sucesso = agendamento_repo.delete(cod_agendamento)
        
        if not sucesso:
            raise HTTPException(status_code=500, detail="Erro ao excluir agendamento")
        
        # Decrementa a quantidade de doadores na agenda se encontrada
        if agenda_encontrada:
            agenda_repo.decrementar_doadores(agenda_encontrada.cod_agenda)
        
        return {
            "success": True,
            "message": "Agendamento excluído com sucesso!"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir agendamento: {str(e)}")