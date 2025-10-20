import datetime
from fastapi import APIRouter, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from data.repo import agendamento_repo, unidade_coleta_repo, doador_repo, doacao_repo, usuario_repo
from data.model.doacao_model import Doacao
from data.model.doador_model import Doador
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

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
        doador = doador_repo.obter_por_id(agendamento.cod_usuario) if agendamento.cod_usuario else None
        usuario_doador = usuario_repo.obter_por_id(agendamento.cod_usuario) if agendamento.cod_usuario else None
        
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
async def confirmar_presenca_agendamento(request: Request, cod_agendamento: int = Body(...), cod_doador: int = Body(...), usuario_logado: dict = None):
    try:
        # Verificar se o agendamento existe
        agendamento = agendamento_repo.obter_por_id(cod_agendamento)
        if not agendamento:
            return JSONResponse(content={
                "success": False,
                "message": f"Agendamento com código {cod_agendamento} não encontrado."
            }, status_code=400)
        
        # Usar o cod_usuario do agendamento (doador da lista)
        cod_usuario_agendamento = agendamento.cod_usuario
        
        # Verificar se o doador (usuário do agendamento) existe na tabela doador
        doador = doador_repo.obter_por_id(cod_usuario_agendamento)
        
        # Se o doador não existe, criar um novo registro
        if not doador:
            novo_doador = Doador(
                cod_doador=cod_usuario_agendamento,
                tipo_sanguineo='O',  # valor padrão
                fator_rh='+',  # valor padrão
                elegivel='sim',
                altura=1.70,
                peso=70,
                profissao='Não informado',
                contato_emergencia='Não informado',
                telefone_emergencia='Não informado'
            )
            try:
                doador_repo.inserir(novo_doador)
                print(f"✅ Doador criado automaticamente: cod_doador={cod_usuario_agendamento}")
            except Exception as e:
                return JSONResponse(content={
                    "success": False,
                    "message": f"Erro ao criar doador: {str(e)}"
                }, status_code=500)
        
        # Criar nova doação com o cod_doador correto
        nova_doacao = Doacao(
            cod_doacao=None,  # Será gerado pelo banco de dados
            cod_doador=cod_usuario_agendamento,
            cod_agendamento=cod_agendamento,
            data_hora=datetime.datetime.now(),
            quantidade=0,  # Será preenchido posteriormente
            status=0,  # Status pendente
            observacoes="Doação criada automaticamente ao confirmar presença"
        )
        
        # Inserir doação no banco
        doacao_repo.inserir(nova_doacao)
        
        # Atualizar status do agendamento para concluído
        agendamento.status = 1  # Concluído
        agendamento_repo.update(agendamento)
        
        return JSONResponse(content={
            "success": True,
            "message": "Presença confirmada e doação criada com sucesso!"
        })
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "message": f"Erro ao confirmar presença: {str(e)}"
        }, status_code=500)
