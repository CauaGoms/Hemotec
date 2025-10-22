from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import unidade_coleta_repo, agenda_repo, colaborador_repo
from data.model.agenda_model import Agenda
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/disponibilidade_coleta")
@requer_autenticacao(["colaborador"])
async def get_colaborador_disponibilidade_coleta(request: Request, usuario_logado: dict = None):
    # Buscar todas as unidades de coleta disponíveis
    unidades = unidade_coleta_repo.obter_todos() or []
    
    response = templates.TemplateResponse(
        "colaborador/colaborador_disponibilidade_coleta.html", 
        {
            "request": request, 
            "active_page": "disponibilidade",
            "usuario": usuario_logado,
            "unidades": unidades
        }
    )
    return response

@router.post("/api/colaborador/disponibilidade-coleta")
@requer_autenticacao(["colaborador"])
async def post_disponibilidade_coleta(request: Request, usuario_logado: dict = None):
    """
    Salva múltiplos horários disponíveis na tabela agenda
    """
    try:
        data = await request.json()
        agendamentos = data.get('agendamentos', [])
        
        if not agendamentos:
            return JSONResponse(
                content={
                    "success": False,
                    "message": "Nenhum agendamento informado"
                },
                status_code=400
            )
        
        # Inserir cada agendamento na tabela agenda
        inserted_count = 0
        for agendamento_data in agendamentos:
            try:
                # Converte strings para objetos date e time
                data_agenda = datetime.strptime(agendamento_data['data_agenda'], '%Y-%m-%d').date()
                hora_agenda = datetime.strptime(agendamento_data['hora_agenda'], '%H:%M:%S').time()
                
                # Cria objeto Agenda
                agenda = Agenda(
                    cod_agenda=None,  # Será gerado automaticamente
                    cod_unidade=agendamento_data['cod_unidade'],
                    cod_agendamento=None,  # Null pois ainda não há agendamento
                    data_agenda=data_agenda,
                    hora_agenda=hora_agenda,
                    vagas=agendamento_data['vagas'],
                    quantidade_doadores=0  # Começa com 0 doadores
                )
                
                # Insere no banco
                cod_agenda = agenda_repo.inserir(agenda)
                if cod_agenda:
                    inserted_count += 1
                    
            except Exception as e:
                import sys
                sys.stderr.write(f"Erro ao inserir agendamento: {str(e)}\n")
                sys.stderr.flush()
                continue
        
        if inserted_count > 0:
            return JSONResponse(
                content={
                    "success": True,
                    "message": f"{inserted_count} horários disponibilizados com sucesso!",
                    "inserted_count": inserted_count
                },
                status_code=200
            )
        else:
            return JSONResponse(
                content={
                    "success": False,
                    "message": "Nenhum horário foi inserido"
                },
                status_code=500
            )
            
    except Exception as e:
        import sys
        sys.stderr.write(f"Erro ao processar disponibilidade: {str(e)}\n")
        sys.stderr.flush()
        return JSONResponse(
            content={
                "success": False,
                "message": f"Erro ao processar requisição: {str(e)}"
            },
            status_code=500
        )
