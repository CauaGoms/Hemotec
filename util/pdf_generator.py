"""
Gerador de PDF para comprovante de doação
"""
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas


def gerar_pdf_comprovante(doacao_data: dict) -> BytesIO:
    """
    Gera um PDF formatado do comprovante de doação
    
    Args:
        doacao_data: Dicionário com dados da doação
        
    Returns:
        BytesIO com o conteúdo do PDF
    """
    buffer = BytesIO()
    
    # Criar documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    # Container para os elementos
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo customizado para título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulo
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        alignment=TA_LEFT
    )
    
    # Cabeçalho
    elements.append(Spacer(1, 10*mm))
    
    # Título principal
    title = Paragraph("COMPROVANTE DE DOAÇÃO DE SANGUE", title_style)
    elements.append(title)
    
    # Subtítulo
    subtitle = Paragraph("Sistema Hemotec - Documento Oficial", subtitle_style)
    elements.append(subtitle)
    
    elements.append(Spacer(1, 10*mm))
    
    # Box de validação
    validation_text = Paragraph(
        "<b>Este comprovante é válido em todo o território nacional</b><br/>"
        "Doação registrada e validada pelo sistema Hemotec",
        subtitle_style
    )
    elements.append(validation_text)
    
    elements.append(Spacer(1, 10*mm))
    
    # Tabela com informações da doação
    data = [
        ['Doador:', doacao_data.get('nome_doador', '')],
        ['Código da Doação:', f"#{doacao_data.get('cod_doacao', '')}"],
        ['Data e Hora:', doacao_data.get('data_formatada', '')],
        ['Tipo Sanguíneo:', doacao_data.get('tipo_sanguineo_completo', '')],
        ['Quantidade Coletada:', f"{doacao_data.get('quantidade', '')}ml"],
        ['Status:', 'Concluída'],
        ['', ''],
        ['Unidade de Coleta:', doacao_data.get('nome_unidade', '')],
        ['Endereço:', doacao_data.get('endereco_completo', '')],
        ['Cidade/Estado:', f"{doacao_data.get('nome_cidade', '')}/{doacao_data.get('sigla_estado', '')}"],
        ['CEP:', doacao_data.get('cep_unidade', '')],
        ['Telefone:', doacao_data.get('telefone_unidade', '')],
    ]
    
    # Criar tabela
    table = Table(data, colWidths=[60*mm, 110*mm])
    
    # Estilo da tabela
    table.setStyle(TableStyle([
        # Cabeçalhos (coluna esquerda)
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, -1), 11),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (0, -1), 10),
        
        # Valores (coluna direita)
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#333333')),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (1, -1), 11),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('LEFTPADDING', (1, 0), (1, -1), 10),
        
        # Separador
        ('BACKGROUND', (0, 6), (1, 6), colors.white),
        ('LINEABOVE', (0, 7), (1, 7), 2, colors.HexColor('#667eea')),
        
        # Bordas
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#667eea')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
        
        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(table)
    
    elements.append(Spacer(1, 15*mm))
    
    # Informações importantes
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        spaceAfter=5,
        alignment=TA_LEFT
    )
    
    info_title = Paragraph("<b>Informações Importantes:</b>", normal_style)
    elements.append(info_title)
    
    info1 = Paragraph("• Este comprovante confirma a realização da doação de sangue.", info_style)
    elements.append(info1)
    
    info2 = Paragraph("• Guarde este documento para apresentação quando necessário.", info_style)
    elements.append(info2)
    
    info3 = Paragraph("• Homens podem doar novamente após 60 dias.", info_style)
    elements.append(info3)
    
    info4 = Paragraph("• Mulheres podem doar novamente após 90 dias.", info_style)
    elements.append(info4)
    
    elements.append(Spacer(1, 15*mm))
    
    # Rodapé
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#999999'),
        alignment=TA_CENTER
    )
    
    data_geracao = datetime.now().strftime('%d/%m/%Y às %H:%M:%S')
    footer = Paragraph(
        f"Documento gerado em {data_geracao}<br/>"
        "Sistema Hemotec - Gestão de Doações de Sangue<br/>"
        "www.hemotec.com.br | pihemotec@gmail.com | (28) 3333-4444",
        footer_style
    )
    elements.append(footer)
    
    # Construir PDF
    doc.build(elements)
    
    # Retornar buffer
    buffer.seek(0)
    return buffer
