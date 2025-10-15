from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from util.formatacoes import formatar_cpf, formatar_data, formatar_tipo_sanguineo
from datetime import datetime
from data.repo import doador_repo, doacao_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/carteira")
@requer_autenticacao(["doador"])
async def get_doador_carteira(request: Request, usuario_logado: dict = None):
    # Criar cópia do usuário para não modificar o original da sessão
    usuario_formatado = usuario_logado.copy() if usuario_logado else {}
    
    # Buscar dados do doador no banco
    cod_usuario = usuario_logado.get("cod_usuario")
    doador = None
    tipo_sanguineo_completo = "N/A"
    ultima_doacao = "Nenhuma doação registrada"
    
    if cod_usuario:
        # Buscar informações do doador (tipo sanguíneo e fator RH)
        doador = doador_repo.obter_por_id(cod_usuario)
        if doador:
            # Formatar tipo sanguíneo (ex: A+, O-, AB+, etc)
            tipo_sanguineo_completo = formatar_tipo_sanguineo(doador.tipo_sanguineo, doador.fator_rh)
        
        # Buscar última doação
        doacoes = doacao_repo.obter_doacoes_completas_por_doador(cod_usuario)
        if doacoes:
            # Pegar a doação mais recente (assumindo que vem ordenada)
            ultima_doacao_data = doacoes[0].get('data_hora')
            if ultima_doacao_data:
                if isinstance(ultima_doacao_data, datetime):
                    ultima_doacao = ultima_doacao_data.strftime('%d/%m/%Y')
                elif isinstance(ultima_doacao_data, str):
                    # Tentar formatar se for string
                    try:
                        data_obj = datetime.strptime(ultima_doacao_data, '%Y-%m-%d %H:%M:%S')
                        ultima_doacao = data_obj.strftime('%d/%m/%Y')
                    except ValueError:
                        try:
                            data_obj = datetime.strptime(ultima_doacao_data, '%Y-%m-%d')
                            ultima_doacao = data_obj.strftime('%d/%m/%Y')
                        except ValueError:
                            ultima_doacao = ultima_doacao_data
    
    # Formatar data de nascimento
    if "data_nascimento" in usuario_formatado:
        usuario_formatado["data_nascimento"] = formatar_data(usuario_formatado["data_nascimento"])
    
    # Formatar CPF
    if "cpf" in usuario_formatado:
        usuario_formatado["cpf"] = formatar_cpf(usuario_formatado["cpf"])
    
    response = templates.TemplateResponse("doador/doador_carteira.html", {
        "request": request, 
        "active_page": "carteira", 
        "usuario": usuario_formatado,
        "tipo_sanguineo": tipo_sanguineo_completo,
        "ultima_doacao": ultima_doacao,
        "cod_doador": cod_usuario
    })
    return response