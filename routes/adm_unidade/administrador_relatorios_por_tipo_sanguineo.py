from fastapi import APIRouter, Request, Query
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import doacao_repo, estoque_repo, doador_repo
from typing import Optional
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/relatorios/tipo_sanguineo")
@requer_autenticacao(["administrador"])
async def get_administrador_relatorio_por_tipo_sanguineo(
    request: Request,
    tipo_sanguineo: Optional[str] = None,
    usuario_logado: dict = None
):
    # Buscar dados
    doacoes = doacao_repo.obter_todos()
    estoque = estoque_repo.obter_todos()
    doadores = doador_repo.obter_todos()
    
    # Se tipo sanguíneo especificado, filtrar
    if tipo_sanguineo and tipo_sanguineo != "todos":
        doacoes_filtradas = []
        for doacao in doacoes:
            doador = next((d for d in doadores if d.cod_doador == doacao.cod_doador), None)
            if doador and doador.tipo_sanguineo == tipo_sanguineo:
                doacoes_filtradas.append(doacao)
        doacoes = doacoes_filtradas
        
        estoque_filtrado = [e for e in estoque if e.tipo_sanguineo == tipo_sanguineo]
        estoque = estoque_filtrado
    
    # Agrupar estatísticas por tipo sanguíneo
    tipos_sanguineos = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    estatisticas = {}
    
    for tipo in tipos_sanguineos:
        # Contar doações deste tipo
        doacoes_tipo = []
        for doacao in doacao_repo.obter_todos():
            doador = next((d for d in doadores if d.cod_doador == doacao.cod_doador), None)
            if doador and doador.tipo_sanguineo == tipo:
                doacoes_tipo.append(doacao)
        
        # Estoque deste tipo
        estoque_tipo = next((e for e in estoque_repo.obter_todos() if e.tipo_sanguineo == tipo), None)
        quantidade_estoque = estoque_tipo.quantidade if estoque_tipo else 0
        
        # Doadores deste tipo
        doadores_tipo = [d for d in doadores if d.tipo_sanguineo == tipo]
        
        estatisticas[tipo] = {
            "total_doacoes": len(doacoes_tipo),
            "quantidade_estoque": quantidade_estoque,
            "total_doadores": len(doadores_tipo),
            "doacoes": doacoes_tipo if tipo_sanguineo == tipo else []
        }
    
    response = templates.TemplateResponse(
        "adm_unidade/administrador_relatorios_por_tipo_sanguineo.html", 
        {
            "request": request,
            "active_page": "relatorio",
            "usuario": usuario_logado,
            "tipo_sanguineo_filtro": tipo_sanguineo or "todos",
            "tipos_sanguineos": tipos_sanguineos,
            "estatisticas": estatisticas,
            "doacoes": doacoes,
            "estoque": estoque
        }
    )
    return response

@router.get("/administrador/relatorios/tipo_sanguineo/pdf")
@requer_autenticacao(["administrador"])
async def get_relatorio_tipo_sanguineo_pdf(
    tipo_sanguineo: str = Query(default="todos"),
    usuario_logado: dict = None
):
    # Buscar dados
    doacoes = doacao_repo.obter_todos()
    estoque = estoque_repo.obter_todos()
    doadores = doador_repo.obter_todos()
    
    # Filtrar se necessário
    if tipo_sanguineo != "todos":
        doacoes_filtradas = []
        for doacao in doacoes:
            doador = next((d for d in doadores if d.cod_doador == doacao.cod_doador), None)
            if doador and doador.tipo_sanguineo == tipo_sanguineo:
                doacoes_filtradas.append(doacao)
        doacoes = doacoes_filtradas
        estoque = [e for e in estoque if e.tipo_sanguineo == tipo_sanguineo]
    
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
    elements.append(Paragraph(f"Relatório por Tipo Sanguíneo", title_style))
    elements.append(Paragraph(f"Tipo: {tipo_sanguineo}", styles['Normal']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Estatísticas
    elements.append(Paragraph(f"<b>Total de Doações:</b> {len(doacoes)}", styles['Normal']))
    if estoque:
        total_estoque = sum([e.quantidade for e in estoque])
        elements.append(Paragraph(f"<b>Estoque Total:</b> {total_estoque} unidades", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabela de estoque
    if estoque:
        elements.append(Paragraph("<b>Estoque por Tipo Sanguíneo</b>", styles['Heading2']))
        data = [["Tipo Sanguíneo", "Quantidade"]]
        for e in estoque:
            data.append([e.tipo_sanguineo, str(e.quantidade)])
        
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
            "Content-Disposition": f"attachment; filename=relatorio_tipo_sanguineo_{tipo_sanguineo}.pdf"
        }
    )