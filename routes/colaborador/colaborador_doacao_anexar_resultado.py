from fastapi import APIRouter, Request, HTTPException, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from datetime import datetime

from data.repo import doacao_repo, doador_repo, usuario_repo
from data.model.doacao_model import Doacao
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/doacao/anexar_resultado/{cod_doacao}")
@requer_autenticacao(["colaborador"])
async def get_colaborador_doacao_anexar_resultado(request: Request, cod_doacao: int, usuario_logado: dict = None):
    """
    Exibe o formulário para anexar exames de uma doação.
    A doação deve estar no status 2 (aguardando exames).
    """
    try:
        # Obter a doação específica
        doacao = doacao_repo.obter_por_id(cod_doacao)
        if not doacao:
            raise HTTPException(status_code=404, detail="Doação não encontrada")
        
        # Verificar se está no status correto (aguardando exames)
        if doacao.status != 2:
            raise HTTPException(status_code=400, detail="Esta doação não está aguardando exames")
        
        # Obter dados do doador
        doador = doador_repo.obter_por_id(doacao.cod_doador)
        usuario_doador = usuario_repo.obter_por_id(doacao.cod_doador)
        
        response = templates.TemplateResponse(
            "colaborador/colaborador_doacao_anexar_resultado.html",
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
        print(f"Erro ao obter página de anexar exames: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/colaborador/doacao/anexar_resultado/{cod_doacao}")
@requer_autenticacao(["colaborador"])
async def post_colaborador_doacao_anexar_resultado(
    request: Request,
    cod_doacao: int,
    exame_hiv: str = Form(...),
    exame_hepatite_b: str = Form(...),
    exame_hepatite_c: str = Form(...),
    exame_sifilis: str = Form(...),
    observacoes_exames: str = Form(""),
    arquivo_exame: UploadFile = File(...),
    usuario_logado: dict = None
):
    """
    Salva os resultados dos exames, arquivo do exame e altera o status para 3 (concluída).
    """
    try:
        # Validar doação
        doacao = doacao_repo.obter_por_id(cod_doacao)
        if not doacao:
            raise HTTPException(status_code=404, detail="Doação não encontrada")
        
        # Validar que todos os exames foram preenchidos
        exames = [exame_hiv, exame_hepatite_b, exame_hepatite_c, exame_sifilis]
        if not all(exame in ["aprovado", "reprovado", "inconcluso"] for exame in exames):
            raise HTTPException(status_code=400, detail="Todos os exames devem ser aprovados, reprovados ou inconclusos")
        
        # Salvar arquivo do exame
        arquivo_path = None
        if arquivo_exame:
            # Criar pasta de exames se não existir
            exames_dir = "static/uploads/exames"
            if not os.path.exists(exames_dir):
                os.makedirs(exames_dir)
            
            # Validar extensão
            extensoes_permitidas = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.jpg', '.jpeg', '.png'}
            _, ext = os.path.splitext(arquivo_exame.filename)
            if ext.lower() not in extensoes_permitidas:
                raise HTTPException(status_code=400, detail=f"Extensão {ext} não permitida")
            
            # Gerar nome único para o arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"exame_{cod_doacao}_{timestamp}{ext}"
            arquivo_path = os.path.join(exames_dir, nome_arquivo)
            
            # Salvar arquivo
            conteudo = await arquivo_exame.read()
            with open(arquivo_path, "wb") as f:
                f.write(conteudo)
        
        # Atualizar doação com status 3 (concluída)
        observacoes_atualizadas = f"{doacao.observacoes}\n\nExames: HIV={exame_hiv}, Hepatite B={exame_hepatite_b}, Hepatite C={exame_hepatite_c}, Sífilis={exame_sifilis}"
        
        if observacoes_exames:
            observacoes_atualizadas += f"\nObservações: {observacoes_exames}"
        
        if arquivo_path:
            observacoes_atualizadas += f"\nArquivo do Exame: {arquivo_path}"
        
        doacao_atualizada = Doacao(
            cod_doacao=cod_doacao,
            cod_doador=doacao.cod_doador,
            cod_agendamento=doacao.cod_agendamento,
            data_hora=doacao.data_hora,
            quantidade=doacao.quantidade,
            status=3,  # Status 3 = concluída
            observacoes=observacoes_atualizadas
        )
        
        sucesso = doacao_repo.update(doacao_atualizada)
        
        if sucesso:
            return RedirectResponse(url=f"/colaborador/doacao/detalhe/{cod_doacao}", status_code=303)
        else:
            # Se falhar, deletar arquivo
            if arquivo_path and os.path.exists(arquivo_path):
                os.remove(arquivo_path)
            raise HTTPException(status_code=500, detail="Erro ao salvar exames")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao anexar exames: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
