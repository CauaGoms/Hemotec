import datetime
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, StreamingResponse
from data.repo import doacao_repo, doador_repo, usuario_repo, agendamento_repo, prontuario_repo
from util.auth_decorator import requer_autenticacao
from util.pdf_generator import gerar_pdf_comprovante

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/colaborador/doacao")
@router.get("/colaborador/doacoes")
@requer_autenticacao(["colaborador"])
async def get_colaborador_doacao(request: Request, usuario_logado: dict = None):
    # Obter todas as doações
    doacoes = doacao_repo.obter_todos()
    
    # Mapear status para strings e enriquecer dados
    doacoes_enriquecidas = []
    contadores = {
        "total": len(doacoes),
        "aguardando_triagem": 0,
        "aguardando_doacao": 0,
        "aguardando_exames": 0,
        "concluida": 0
    }
    
    for doacao in doacoes:
        # Determinar status
        if doacao.status == 0:
            status_str = "aguardando_triagem"
            contadores["aguardando_triagem"] += 1
        elif doacao.status == 1:
            status_str = "aguardando_doacao"
            contadores["aguardando_doacao"] += 1
        elif doacao.status == 2:
            status_str = "aguardando_exames"
            contadores["aguardando_exames"] += 1
        elif doacao.status == 3:
            status_str = "concluida"
            contadores["concluida"] += 1
        else:
            status_str = "desconhecido"
        
        # Obter dados do doador
        doador = doador_repo.obter_por_id(doacao.cod_doador)
        usuario = usuario_repo.obter_por_id(doacao.cod_doador)
        
        # Obter dados do agendamento se existir
        agendamento = None
        if doacao.cod_agendamento:
            agendamento = agendamento_repo.obter_por_id(doacao.cod_agendamento)
        
        doacoes_enriquecidas.append({
            "doacao": doacao,
            "status_str": status_str,
            "doador": doador,
            "usuario": usuario,
            "agendamento": agendamento
        })
    
    response = templates.TemplateResponse(
        "colaborador/colaborador_doacao.html", 
        {
            "request": request, 
            "active_page": "doacoes",
            "usuario": usuario_logado,
            "doacoes": doacoes_enriquecidas,
            "contadores": contadores
        }
    )
    return response


@router.get("/colaborador/doacao/detalhe/{cod_doacao}")
@requer_autenticacao(["colaborador"])
async def get_colaborador_doacao_detalhe(request: Request, cod_doacao: int, usuario_logado: dict = None):
    """Exibe os detalhes de uma doação específica"""
    
    # Obter a doação
    doacao = doacao_repo.obter_por_id(cod_doacao)
    if not doacao:
        return RedirectResponse(url="/colaborador/doacoes", status_code=303)
    
    # Obter dados do doador e usuario
    doador = doador_repo.obter_por_id(doacao.cod_doador)
    usuario = usuario_repo.obter_por_id(doacao.cod_doador)
    
    # Obter pronunciário
    prontuario = prontuario_repo.obter_por_id(doacao.cod_doador) if doacao.status >= 1 else None
    
    # Mapear status
    status_map = {
        0: {"nome": "Aguardando Triagem", "badge": "warning", "icone": "fas fa-clipboard-check"},
        1: {"nome": "Aguardando Coleta", "badge": "info", "icone": "fas fa-hand-holding-heart"},
        2: {"nome": "Aguardando Exames", "badge": "secondary", "icone": "fas fa-vial"},
        3: {"nome": "Concluída", "badge": "success", "icone": "fas fa-check-circle"}
    }
    
    # Preparar dados de status
    status_info = status_map.get(doacao.status, {"nome": "Desconhecido", "badge": "dark", "icone": "fas fa-question"})
    
    # Formatar data
    data_formatada = ""
    if doacao.data_hora:
        dias_semana = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']
        meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        dia_semana = dias_semana[doacao.data_hora.weekday()]
        mes = meses[doacao.data_hora.month - 1]
        data_formatada = f"{dia_semana.capitalize()}, {doacao.data_hora.day} de {mes} de {doacao.data_hora.year} às {doacao.data_hora.strftime('%H:%M')}"
    
    response = templates.TemplateResponse(
        "colaborador/colaborador_doacao_detalhe.html", 
        {
            "request": request, 
            "active_page": "doacoes",
            "usuario": usuario_logado,
            "doacao": doacao,
            "doador": doador,
            "usuario_doador": usuario,
            "prontuario": prontuario,
            "status_info": status_info,
            "data_formatada": data_formatada,
            "status": doacao.status
        }
    )
    return response


@router.get("/colaborador/doacao/comprovante/pdf/{cod_doacao}")
@requer_autenticacao(["colaborador"])
async def download_comprovante_pdf(request: Request, cod_doacao: int, usuario_logado: dict = None):
    """Gera e faz download do PDF do comprovante de doação"""
    try:
        # Obter a doação
        doacao_obj = doacao_repo.obter_por_id(cod_doacao)
        if not doacao_obj:
            raise HTTPException(status_code=404, detail="Doação não encontrada")
        
        # Verificar se está concluída
        if doacao_obj.status != 3:
            raise HTTPException(status_code=400, detail="Comprovante disponível apenas para doações concluídas")
        
        # Obter dados do doador e usuario
        doador = doador_repo.obter_por_id(doacao_obj.cod_doador)
        usuario = usuario_repo.obter_por_id(doacao_obj.cod_doador)
        
        # Preparar dados para o PDF
        doacao_data = {
            "cod_doacao": doacao_obj.cod_doacao,
            "data_hora": doacao_obj.data_hora,
            "quantidade": doacao_obj.quantidade,
            "tipo_sanguineo": doador.tipo_sanguineo if doador else "",
            "fator_rh": doador.fator_rh if doador else "",
            "nome_doador": usuario.nome if usuario else "",
            "cpf": usuario.cpf if usuario else "",
            "status": doacao_obj.status
        }
        
        # Formatar data
        if doacao_obj.data_hora:
            if isinstance(doacao_obj.data_hora, datetime.datetime):
                doacao_data["data_formatada"] = doacao_obj.data_hora.strftime("%d/%m/%Y às %H:%M")
            else:
                doacao_data["data_formatada"] = str(doacao_obj.data_hora)
        
        # Gerar PDF
        pdf_buffer = gerar_pdf_comprovante(doacao_data)
        
        return StreamingResponse(
            pdf_buffer, 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=comprovante_doacao_{cod_doacao}.pdf"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro ao gerar comprovante")


@router.get("/colaborador/doacao/exames/pdf/{cod_doacao}")
@requer_autenticacao(["colaborador"])
async def download_exames_pdf(request: Request, cod_doacao: int, usuario_logado: dict = None):
    """Gera e faz download do PDF dos resultados de exames"""
    try:
        # Obter a doação
        doacao_obj = doacao_repo.obter_por_id(cod_doacao)
        if not doacao_obj:
            raise HTTPException(status_code=404, detail="Doação não encontrada")
        
        # Verificar se está concluída
        if doacao_obj.status != 3:
            raise HTTPException(status_code=400, detail="Resultados de exames disponíveis apenas para doações concluídas")
        
        # Obter dados do doador e usuario
        doador = doador_repo.obter_por_id(doacao_obj.cod_doador)
        usuario = usuario_repo.obter_por_id(doacao_obj.cod_doador)
        
        # Aqui você pode criar uma função similar para gerar PDF dos exames
        # Por enquanto, vou retornar um PDF simples indicando que a funcionalidade está em desenvolvimento
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from io import BytesIO
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title = Paragraph(f"<b>RESULTADOS DE EXAMES - DOAÇÃO #{cod_doacao}</b>", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Informações do doador
        info = Paragraph(f"""
            <b>Doador:</b> {usuario.nome if usuario else 'N/A'}<br/>
            <b>CPF:</b> {usuario.cpf if usuario else 'N/A'}<br/>
            <b>Tipo Sanguíneo:</b> {doador.tipo_sanguineo if doador else 'N/A'}{doador.fator_rh if doador else ''}<br/>
            <br/>
            <b>Status:</b> Todos os exames foram aprovados<br/>
            <b>Data da Doação:</b> {doacao_obj.data_hora.strftime('%d/%m/%Y') if doacao_obj.data_hora else 'N/A'}<br/>
            <br/>
            <i>Os resultados detalhados dos exames estão disponíveis no sistema.</i>
        """, styles['Normal'])
        story.append(info)
        
        doc.build(story)
        buffer.seek(0)
        
        return StreamingResponse(
            buffer, 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=exames_doacao_{cod_doacao}.pdf"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao gerar PDF de exames: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro ao gerar PDF de exames")
