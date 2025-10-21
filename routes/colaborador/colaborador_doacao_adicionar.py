from datetime import datetime
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from data.model.doacao_model import Doacao
from data.repo import doacao_repo, doador_repo, usuario_repo, agendamento_repo
from util.auth_decorator import requer_autenticacao
from util.database import get_connection

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/doacao/adicionar")
@requer_autenticacao(["colaborador"])
async def get_colaborador_doacao_adicionar(request: Request, usuario_logado: dict = None):
    """
    Exibe o formulário para inserir informações de doação.
    A doação deve ter sido criada previamente no agendamento.
    """
    try:
        # Obter lista de agendamentos pendentes de doação
        agendamentos = agendamento_repo.obter_todos()
        agendamentos_pendentes = []
        
        for agendamento in agendamentos:
            # Verificar se existe doação para este agendamento
            doacoes = doacao_repo.obter_todos()
            doacao_existe = any(d.cod_agendamento == agendamento.cod_agendamento for d in doacoes)
            
            if not doacao_existe and agendamento.status == 1:  # Status 1 = confirmado
                doador = doador_repo.obter_por_id(agendamento.cod_usuario)
                usuario_doador = usuario_repo.obter_por_id(agendamento.cod_usuario)
                agendamentos_pendentes.append({
                    "agendamento": agendamento,
                    "doador": doador,
                    "usuario": usuario_doador
                })
        
        response = templates.TemplateResponse(
            "colaborador/colaborador_doacao_adicionar.html",
            {
                "request": request,
                "active_page": "doacoes",
                "usuario": usuario_logado,
                "agendamentos": agendamentos_pendentes
            }
        )
        return response
    except Exception as e:
        print(f"Erro ao obter página de adição de doação: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/colaborador/doacao/adicionar")
@requer_autenticacao(["colaborador"])
async def post_colaborador_doacao_adicionar(
    request: Request,
    cod_agendamento: int = Form(...),
    data_hora: str = Form(...),
    quantidade: int = Form(...),
    observacoes: str = Form(""),
    usuario_logado: dict = None
):
    """
    Completa a informação da doação (data_hora, quantidade, observações)
    e altera o status para 3 (concluída).
    """
    try:
        # Validar agendamento
        agendamento = agendamento_repo.obter_por_id(cod_agendamento)
        if not agendamento:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        # Converter data_hora string para datetime
        try:
            data_hora_obj = datetime.fromisoformat(data_hora)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido")
        
        # Validar quantidade
        if quantidade <= 0 or quantidade > 500:
            raise HTTPException(status_code=400, detail="Quantidade deve ser entre 1 e 500ml")
        
        # Criar nova doação com status 3 (concluída)
        doacao = Doacao(
            cod_doacao=None,
            cod_doador=agendamento.cod_usuario,
            cod_agendamento=cod_agendamento,
            data_hora=data_hora_obj,
            quantidade=quantidade,
            status=3,  # Status 3 = concluída
            observacoes=observacoes
        )
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cod_doacao = doacao_repo.inserir(doacao, cursor)
            conn.commit()
        
        if cod_doacao:
            return RedirectResponse(url=f"/colaborador/doacao/detalhe/{cod_doacao}", status_code=303)
        else:
            raise HTTPException(status_code=500, detail="Erro ao salvar doação")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao inserir doação: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))