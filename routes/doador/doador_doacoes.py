from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import doacao_repo
import locale

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Configurar locale para português (tente diferentes opções)
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
        except:
            pass  # Mantém o locale padrão se não conseguir configurar

@router.get("/doador/doacoes")
@requer_autenticacao(["doador"])
async def get_doador_doacoes(request: Request, usuario_logado: dict = None):
    # Obter cod_doador do usuário logado (cod_doador = cod_usuario)
    cod_doador = usuario_logado.get("cod_usuario")
    
    # Buscar doações completas do doador
    doacoes = doacao_repo.obter_doacoes_completas_por_doador(cod_doador)
    
    # Mapear status para classes CSS
    status_map = {
        0: {'classe': 'canceled', 'badge': 'canceled-badge', 'nome': 'Cancelada', 'icone': 'fa-times-circle'},
        1: {'classe': 'refused', 'badge': 'refused-badge', 'nome': 'Recusada', 'icone': 'fa-exclamation-triangle'},
        2: {'classe': 'pending', 'badge': 'pending-badge', 'nome': 'Aguardando Exame', 'icone': 'fa-hourglass-half'},
        3: {'classe': 'completed', 'badge': 'completed-badge', 'nome': 'Concluída', 'icone': 'fa-check-circle'}
    }
    
    # Mapeamento de dias da semana e meses em português
    dias_semana = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira', 
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    
    meses = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
        'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
        'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
        'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
    }
    
    # Adicionar informações de CSS e formatação para cada doação
    for doacao in doacoes:
        status_info = status_map.get(doacao['status'], status_map[2])
        doacao['status_classe'] = status_info['classe']
        doacao['status_badge'] = status_info['badge']
        doacao['status_nome'] = status_info['nome']
        doacao['status_icone'] = status_info['icone']
        
        # Formatar data em português
        if doacao['data_hora']:
            dt = doacao['data_hora']
            dia_semana_en = dt.strftime('%A')
            mes_en = dt.strftime('%B')
            dia_semana_pt = dias_semana.get(dia_semana_en, dia_semana_en)
            mes_pt = meses.get(mes_en, mes_en)
            doacao['data_formatada'] = f"{dia_semana_pt}, {dt.day} de {mes_pt} de {dt.year} - {dt.strftime('%H:%M')}"
        else:
            doacao['data_formatada'] = 'Data não disponível'
    
    response = templates.TemplateResponse(
        "doador/doador_doacoes.html", 
        {
            "request": request, 
            "active_page": "doacoes", 
            "usuario": usuario_logado,
            "doacoes": doacoes
        }
    )
    return response