from fastapi import APIRouter, Request, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import agendamento_repo, unidade_coleta_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/agendamento/alterar/{cod_agendamento}")
@requer_autenticacao(["doador"])
async def get_doador_agendamento_alterar(request: Request, cod_agendamento: int, usuario_logado: dict = None):
    # Buscar o agendamento
    agendamento = agendamento_repo.obter_por_id(cod_agendamento)
    
    # Verificar se o agendamento existe
    if not agendamento:
        return RedirectResponse("/doador/agendamento?erro=agendamento_nao_encontrado", status_code=status.HTTP_303_SEE_OTHER)
    
    # Verificar se o agendamento pertence ao usuário logado (segurança)
    if agendamento.cod_usuario != usuario_logado['cod_usuario']:
        return RedirectResponse("/doador/agendamento?erro=sem_permissao", status_code=status.HTTP_303_SEE_OTHER)
    
    # Buscar a unidade de coleta atual do agendamento
    unidade_atual = unidade_coleta_repo.obter_por_id(agendamento.local_agendamento)
    
    # Buscar todas as unidades de coleta disponíveis
    unidades = unidade_coleta_repo.obter_todos() or []
    
    response = templates.TemplateResponse("doador/doador_agendamento_alterar.html", {
        "request": request, 
        "active_page": "agendamento", 
        "usuario": usuario_logado,
        "agendamento": agendamento,
        "unidade_atual": unidade_atual,
        "unidades": unidades
    })
    return response

@router.post("/doador/agendamento/alterar/{cod_agendamento}")
@requer_autenticacao(["doador"])
async def post_doador_agendamento_alterar(
    request: Request, 
    cod_agendamento: int, 
    data_hora: str = Form(...),
    local_agendamento: str = Form(...),
    usuario_logado: dict = None
):
    from datetime import datetime
    
    # Buscar o agendamento
    agendamento = agendamento_repo.obter_por_id(cod_agendamento)
    
    # Verificar se o agendamento existe
    if not agendamento:
        return RedirectResponse("/doador/agendamento?erro=agendamento_nao_encontrado", status_code=status.HTTP_303_SEE_OTHER)
    
    # Verificar se o agendamento pertence ao usuário logado (segurança)
    if agendamento.cod_usuario != usuario_logado['cod_usuario']:
        return RedirectResponse("/doador/agendamento?erro=sem_permissao", status_code=status.HTTP_303_SEE_OTHER)
    
    # Dados já recebidos via Form
    data_hora_str = data_hora
    local_agendamento_id = local_agendamento
    
    # Validar dados
    if not data_hora_str or not local_agendamento_id:
        return RedirectResponse(f"/doador/agendamento/alterar/{cod_agendamento}?erro=dados_incompletos", status_code=status.HTTP_303_SEE_OTHER)
    
    try:
        # Converter string para datetime
        data_hora_obj = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')
        
        # Atualizar o agendamento
        agendamento.data_hora = data_hora_obj
        agendamento.local_agendamento = int(local_agendamento_id)
        
        # Salvar no banco
        sucesso = agendamento_repo.update(agendamento)
        
        if sucesso:
            return RedirectResponse("/doador/agendamento?sucesso=agendamento_alterado", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse(f"/doador/agendamento/alterar/{cod_agendamento}?erro=falha_atualizacao", status_code=status.HTTP_303_SEE_OTHER)
    
    except ValueError:
        return RedirectResponse(f"/doador/agendamento/alterar/{cod_agendamento}?erro=data_invalida", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao alterar agendamento: {e}")
        return RedirectResponse(f"/doador/agendamento/alterar/{cod_agendamento}?erro=erro_inesperado", status_code=status.HTTP_303_SEE_OTHER)