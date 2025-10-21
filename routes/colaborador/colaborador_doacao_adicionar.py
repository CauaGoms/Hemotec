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

@router.get("/colaborador/doacao/adicionar/{cod_doacao}")
@requer_autenticacao(["colaborador"])
async def get_colaborador_doacao_adicionar(request: Request, cod_doacao: int, usuario_logado: dict = None):
    """
    Exibe o formulário para inserir informações de doação.
    Acessa uma doação específica que está no status aguardando_doacao (status 1).
    """
    try:
        # Obter a doação específica
        doacao = doacao_repo.obter_por_id(cod_doacao)
        if not doacao:
            raise HTTPException(status_code=404, detail="Doação não encontrada")
        
        # Verificar se está no status correto (aguardando coleta)
        if doacao.status != 1:
            raise HTTPException(status_code=400, detail="Esta doação não está aguardando coleta")
        
        # Obter dados do doador
        doador = doador_repo.obter_por_id(doacao.cod_doador)
        usuario_doador = usuario_repo.obter_por_id(doacao.cod_doador)
        
        response = templates.TemplateResponse(
            "colaborador/colaborador_doacao_adicionar.html",
            {
                "request": request,
                "active_page": "doacoes",
                "usuario": usuario_logado,
                "doacao": doacao,
                "doador": doador,
                "usuario_doador": usuario_doador
            }
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao obter página de adição de doação: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/colaborador/doacao/adicionar/{cod_doacao}")
@requer_autenticacao(["colaborador"])
async def post_colaborador_doacao_adicionar(
    request: Request,
    cod_doacao: int,
    data_hora: str = Form(...),
    quantidade: int = Form(...),
    observacoes: str = Form(""),
    usuario_logado: dict = None
):
    """
    Completa a informação da doação (data_hora, quantidade, observações)
    e altera o status para 2 (aguardando exames).
    """
    try:
        # Validar doação
        doacao = doacao_repo.obter_por_id(cod_doacao)
        if not doacao:
            raise HTTPException(status_code=404, detail="Doação não encontrada")
        
        # Converter data_hora string para datetime
        try:
            data_hora_obj = datetime.fromisoformat(data_hora)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido")
        
        # Validar quantidade
        if quantidade <= 0 or quantidade > 500:
            raise HTTPException(status_code=400, detail="Quantidade deve ser entre 1 e 500ml")
        
        # Atualizar doação com dados de coleta e status 2 (aguardando exames)
        doacao_atualizada = Doacao(
            cod_doacao=cod_doacao,
            cod_doador=doacao.cod_doador,
            cod_agendamento=doacao.cod_agendamento,
            data_hora=data_hora_obj,
            quantidade=quantidade,
            status=2,  # Status 2 = aguardando exames
            observacoes=observacoes
        )
        
        sucesso = doacao_repo.update(doacao_atualizada)
        
        if sucesso:
            return RedirectResponse(url=f"/colaborador/doacao/detalhe/{cod_doacao}", status_code=303)
        else:
            raise HTTPException(status_code=500, detail="Erro ao salvar doação")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao inserir dados de doação: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))