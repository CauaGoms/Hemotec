from fastapi import APIRouter, Request, Query
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import colaborador_repo
from datetime import datetime, date
from typing import Optional
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/gestor/relatorio/colaborador")
@requer_autenticacao(["gestor"])
async def get_gestor_relatorio_colaborador(
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
    
    # Buscar todos os colaboradores
    colaboradores = colaborador_repo.obter_todos()
    
    # Filtrar por período de cadastro
    data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d").date()
    
    # Filtrar novos colaboradores no período
    novos_colaboradores = []
    colaboradores_completos = []
    
    for colaborador in colaboradores:
        colab_data = {
            'cod_colaborador': colaborador.cod_colaborador,
            'nome': colaborador.nome,
            'email': colaborador.email,
            'cpf': colaborador.cpf,
            'telefone': colaborador.telefone,
            'funcao': colaborador.funcao,
            'cod_unidade': colaborador.cod_unidade,
            'data_cadastro': colaborador.data_cadastro,
            'status': colaborador.status
        }
        colaboradores_completos.append(colab_data)
        
        # Verificar se é um novo colaborador no período
        if colaborador.data_cadastro and data_inicio_obj <= colaborador.data_cadastro <= data_fim_obj:
            novos_colaboradores.append(colab_data)
    
    # Calcular estatísticas
    total_colaboradores = len(colaboradores_completos)
    novos_colaboradores_periodo = len(novos_colaboradores)
    colaboradores_ativos = len([c for c in colaboradores_completos if c['status']])
    
    # Estatísticas por função
    funcoes = {}
    for colab in colaboradores_completos:
        funcao = colab['funcao'] if colab['funcao'] else 'Não especificada'
        funcoes[funcao] = funcoes.get(funcao, 0) + 1
    
    response = templates.TemplateResponse(
        "gestor/gestor_relatorio_colaborador.html",
        {
            "request": request,
            "active_page": "relatorio",
            "usuario": usuario_logado,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "colaboradores": colaboradores_completos,
            "novos_colaboradores": novos_colaboradores,
            "total_colaboradores": total_colaboradores,
            "novos_colaboradores_periodo": novos_colaboradores_periodo,
            "colaboradores_ativos": colaboradores_ativos,
            "funcoes": funcoes
        }
    )
    return response

@router.get("/gestor/relatorio/colaborador/pdf")
@requer_autenticacao(["gestor"])
async def get_gestor_relatorio_colaborador_pdf(
    data_inicio: str = Query(...),
    data_fim: str = Query(...),
    usuario_logado: dict = None
):
    # Buscar todos os colaboradores
    colaboradores = colaborador_repo.obter_todos()
    
    # Filtrar por período
    data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d").date()
    
    # Filtrar novos colaboradores no período
    novos_colaboradores = []
    for colaborador in colaboradores:
        if colaborador.data_cadastro and data_inicio_obj <= colaborador.data_cadastro <= data_fim_obj:
            novos_colaboradores.append({
                'nome': colaborador.nome,
                'email': colaborador.email,
                'funcao': colaborador.funcao if colaborador.funcao else 'Não especificada',
                'data_cadastro': colaborador.data_cadastro
            })
    
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
    elements.append(Paragraph("Relatório de Colaboradores", title_style))
    elements.append(Paragraph(f"Período: {data_inicio} a {data_fim}", styles['Normal']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Estatísticas
    elements.append(Paragraph(f"<b>Novos Colaboradores no Período:</b> {len(novos_colaboradores)}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabela de novos colaboradores
    if novos_colaboradores:
        elements.append(Paragraph("<b>Novos Colaboradores Cadastrados</b>", styles['Heading2']))
        data = [["Nome", "E-mail", "Função", "Data Cadastro"]]
        for colab in novos_colaboradores[:50]:  # Limitar a 50
            data.append([
                colab['nome'][:30],
                colab['email'][:30],
                colab['funcao'][:20],
                str(colab['data_cadastro'])
            ])
        
        table = Table(data, colWidths=[2*inch, 2*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC143C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("Nenhum novo colaborador cadastrado no período.", styles['Normal']))
    
    doc.build(elements)
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=relatorio_colaboradores_{data_inicio}_{data_fim}.pdf"
        }
    )