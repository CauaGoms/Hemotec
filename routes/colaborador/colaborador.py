from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.repo import usuario_repo, agendamento_repo, doacao_repo, campanha_repo
from datetime import date, datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador")
async def get_colaborador_home(request: Request):
    # Obter usuário da sessão
    email_usuario = request.session.get("user_email")
    usuario = None
    if email_usuario:
        usuario = usuario_repo.obter_por_email(email_usuario)
    
    # Obter agendamentos de hoje
    hoje = date.today()
    todos_agendamentos = agendamento_repo.obter_todos()
    agendamentos_hoje = []
    
    if todos_agendamentos:
        for agendamento in todos_agendamentos:
            if agendamento.data_hora:
                # Extrair apenas a data do datetime
                data_agendamento = agendamento.data_hora.date() if isinstance(agendamento.data_hora, datetime) else agendamento.data_hora
                if data_agendamento == hoje:
                    agendamentos_hoje.append(agendamento)
    
    # Obter doações em andamento (status 2 = aguardando exames, 4 = aguardando doacao, 5 = aguardando triagem)
    todas_doacoes = doacao_repo.obter_todos()
    doacoes_andamento = []
    
    if todas_doacoes:
        for doacao in todas_doacoes:
            if doacao.status in [2, 4, 5]:  # Status de doações em andamento
                doacoes_andamento.append(doacao)
    
    # Obter campanhas ativas (status 1 = ativa)
    todas_campanhas = campanha_repo.obter_todos()
    campanhas_ativas = []
    
    if todas_campanhas:
        for campanha in todas_campanhas:
            if campanha.status == 1:  # Campanha ativa
                campanhas_ativas.append(campanha)
    
    response = templates.TemplateResponse("colaborador/colaborador_inicio.html", {
        "request": request, 
        "active_page": "home",
        "usuario": usuario,
        "agendamentos_hoje": agendamentos_hoje,
        "doacoes_andamento": doacoes_andamento,
        "campanhas_ativas": campanhas_ativas
    })
    return response
