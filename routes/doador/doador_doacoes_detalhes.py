from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, StreamingResponse
from util.auth_decorator import requer_autenticacao
from data.repo import doacao_repo, prontuario_repo, exame_repo
from util.pdf_generator import gerar_pdf_comprovante

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/doador/doacoes/detalhes/{cod_doacao}")
@requer_autenticacao(["doador"])
async def get_doador_doacoes_detalhes(request: Request, cod_doacao: int, usuario_logado: dict = None):
    """
    Exibe detalhes completos de uma doação específica
    O conteúdo varia de acordo com o status da doação
    """
    try:
        # Verificar se a doação pertence ao usuário logado
        cod_doador = usuario_logado.get("cod_usuario")
        
        # Buscar doação completa
        doacoes = doacao_repo.obter_doacoes_completas_por_doador(cod_doador)
        doacao = next((d for d in doacoes if d['cod_doacao'] == cod_doacao), None)
        
        if not doacao:
            # Doação não encontrada ou não pertence ao usuário
            return RedirectResponse(url="/doador/doacoes", status_code=303)
        
        # Buscar prontuário relacionado à doação
        prontuario = prontuario_repo.obter_por_doacao(cod_doacao)
        
        # Buscar exames relacionados à doação
        exames = exame_repo.obter_por_doacao(cod_doacao)
        
        # Mapear status para classe CSS e informações
        status_info = {
            0: {
                'classe': 'cancelada',
                'badge': 'status-canceled',
                'icone': 'fa-ban',
                'nome': 'Cancelada',
                'cor': 'danger'
            },
            1: {
                'classe': 'recusada',
                'badge': 'status-refused',
                'icone': 'fa-times-circle',
                'nome': 'Recusada',
                'cor': 'warning'
            },
            2: {
                'classe': 'aguardando',
                'badge': 'status-pending',
                'icone': 'fa-hourglass-half',
                'nome': 'Aguardando Exame',
                'cor': 'info'
            },
            3: {
                'classe': 'concluida',
                'badge': 'status-completed',
                'icone': 'fa-check-circle',
                'nome': 'Concluída',
                'cor': 'success'
            }
        }
        
        doacao['status_info'] = status_info.get(doacao['status'], status_info[0])
        
        # Formatar data
        if doacao['data_hora']:
            from datetime import datetime
            if isinstance(doacao['data_hora'], datetime):
                doacao['data_formatada'] = doacao['data_hora'].strftime('%d/%m/%Y às %H:%M')
                doacao['data_completa'] = doacao['data_hora'].strftime('%A, %d de %B de %Y')
            else:
                doacao['data_formatada'] = str(doacao['data_hora'])
                doacao['data_completa'] = str(doacao['data_hora'])
        
        response = templates.TemplateResponse(
            "doador/doador_doacoes_detalhes.html",
            {
                "request": request,
                "active_page": "doacoes",
                "usuario": usuario_logado,
                "doacao": doacao,
                "prontuario": prontuario,
                "exames": exames
            }
        )
        return response
        
    except Exception as e:
        print(f"Erro ao buscar detalhes da doação: {e}")
        import traceback
        traceback.print_exc()
        return RedirectResponse(url="/doador/doacoes", status_code=303)

@router.get("/doador/doacoes/comprovante/pdf/{cod_doacao}")
@requer_autenticacao(["doador"])
async def download_comprovante_pdf(request: Request, cod_doacao: int, usuario_logado: dict = None):
    """Gera e faz download do PDF do comprovante de doação"""
    try:
        cod_doador = usuario_logado.get("cod_usuario")
        doacoes = doacao_repo.obter_doacoes_completas_por_doador(cod_doador)
        doacao = next((d for d in doacoes if d["cod_doacao"] == cod_doacao), None)
        if not doacao:
            raise HTTPException(status_code=404, detail="Doação não encontrada")
        if doacao["status"] != 3:
            raise HTTPException(status_code=400, detail="Comprovante disponível apenas para doações concluídas")
        if doacao["data_hora"]:
            from datetime import datetime
            if isinstance(doacao["data_hora"], datetime):
                doacao["data_formatada"] = doacao["data_hora"].strftime("%d/%m/%Y às %H:%M")
            else:
                doacao["data_formatada"] = str(doacao["data_hora"])
        doacao["nome_doador"] = usuario_logado.get("nome", "")
        pdf_buffer = gerar_pdf_comprovante(doacao)
        return StreamingResponse(pdf_buffer, media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=comprovante_doacao_{cod_doacao}.pdf"})
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro ao gerar comprovante")
