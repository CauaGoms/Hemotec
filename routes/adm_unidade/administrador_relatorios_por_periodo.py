from fastapi import APIRouter, Request, Query
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import doacao_repo, agendamento_repo, estoque_repo
from datetime import datetime, date
from typing import Optional
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/relatorios/periodo")
@requer_autenticacao(["administrador"])
async def get_administrador_relatorio_por_periodo(
    request: Request, 
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    usuario_logado: dict = None
):
    # Define período padrão (último mês se não especificado)
    if not data_inicio or not data_fim:
        data_fim_obj = date.today()
        data_inicio_obj = date(data_fim_obj.year, data_fim_obj.month - 1 if data_fim_obj.month > 1 else 12, data_fim_obj.day)
        data_inicio = data_inicio_obj.strftime("%Y-%m-%d")
        data_fim = data_fim_obj.strftime("%Y-%m-%d")
    
    # Buscar dados do período
    doacoes = doacao_repo.obter_todos()
    agendamentos = agendamento_repo.obter_todos()
    estoque = estoque_repo.obter_todos()
    
    # Filtrar por período
    data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d").date()
    
    doacoes_periodo = [d for d in doacoes if d.data_hora and data_inicio_obj <= d.data_hora.date() <= data_fim_obj]
    agendamentos_periodo = [a for a in agendamentos if a.data_hora and data_inicio_obj <= a.data_hora.date() <= data_fim_obj]
    
    # Calcular estatísticas
    total_doacoes = len(doacoes_periodo)
    total_agendamentos = len(agendamentos_periodo)
    agendamentos_confirmados = len([a for a in agendamentos_periodo if a.status == 1])
    agendamentos_cancelados = len([a for a in agendamentos_periodo if a.status == 2])
    
    # Estoque atual
    estoque_total = sum([e.quantidade for e in estoque])
    
    response = templates.TemplateResponse(
        "adm_unidade/administrador_relatorios_por_periodo.html", 
        {
            "request": request,
            "active_page": "relatorio",
            "usuario": usuario_logado,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "doacoes": doacoes_periodo,
            "agendamentos": agendamentos_periodo,
            "total_doacoes": total_doacoes,
            "total_agendamentos": total_agendamentos,
            "agendamentos_confirmados": agendamentos_confirmados,
            "agendamentos_cancelados": agendamentos_cancelados,
            "estoque": estoque,
            "estoque_total": estoque_total
        }
    )
    return response

@router.get("/administrador/relatorios/periodo/pdf")
@requer_autenticacao(["administrador"])
async def get_relatorio_periodo_pdf(
    data_inicio: str = Query(...),
    data_fim: str = Query(...),
    usuario_logado: dict = None
):
    # Buscar dados do período
    doacoes = doacao_repo.obter_todos()
    agendamentos = agendamento_repo.obter_todos()
    
    # Filtrar por período
    data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d").date()
    
    doacoes_periodo = [d for d in doacoes if d.data_hora and data_inicio_obj <= d.data_hora.date() <= data_fim_obj]
    agendamentos_periodo = [a for a in agendamentos if a.data_hora and data_inicio_obj <= a.data_hora.date() <= data_fim_obj]
    
    # Gerar PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#DC143C'),
        spaceAfter=30,
        alignment=1
    )
    elements.append(Paragraph(f"Relatório por Período", title_style))
    elements.append(Paragraph(f"Período: {data_inicio} a {data_fim}", styles['Normal']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Estatísticas
    elements.append(Paragraph(f"<b>Total de Doações:</b> {len(doacoes_periodo)}", styles['Normal']))
    elements.append(Paragraph(f"<b>Total de Agendamentos:</b> {len(agendamentos_periodo)}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabela de doações
    if doacoes_periodo:
        elements.append(Paragraph("<b>Doações do Período</b>", styles['Heading2']))
        data = [["Data", "Doador", "Status"]]
        for doacao in doacoes_periodo[:20]:  # Limitar a 20
            data.append([str(doacao.data_hora.date()) if doacao.data_hora else "-", str(doacao.cod_doador), "Realizada"])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC143C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
    
    doc.build(elements)
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=relatorio_periodo_{data_inicio}_{data_fim}.pdf"
        }
    )