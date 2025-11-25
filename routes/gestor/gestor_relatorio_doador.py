from fastapi import APIRouter, Request, Query
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo import doador_repo, usuario_repo
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

@router.get("/gestor/relatorio/doador")
@requer_autenticacao(["gestor"])
async def get_gestor_relatorio_doador(
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
    
    # Buscar todos os doadores
    doadores = doador_repo.obter_todos()
    usuarios = usuario_repo.obter_todos()
    
    # Criar dicionário de usuários por ID
    usuarios_dict = {u.cod_usuario: u for u in usuarios}
    
    # Filtrar por período de cadastro
    data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d").date()
    
    # Enriquecer doadores com dados do usuário e filtrar por período
    doadores_completos = []
    novos_doadores = []
    
    for doador in doadores:
        usuario = usuarios_dict.get(doador.cod_doador)
        if usuario:
            doador_completo = {
                'cod_doador': doador.cod_doador,
                'nome': usuario.nome,
                'email': usuario.email,
                'cpf': usuario.cpf,
                'telefone': usuario.telefone,
                'tipo_sanguineo': doador.tipo_sanguineo,
                'fator_rh': doador.fator_rh,
                'data_cadastro': usuario.data_cadastro,
                'status': usuario.status,
                'elegivel': doador.elegivel
            }
            doadores_completos.append(doador_completo)
            
            # Verificar se é um novo doador no período
            if usuario.data_cadastro and data_inicio_obj <= usuario.data_cadastro <= data_fim_obj:
                novos_doadores.append(doador_completo)
    
    # Calcular estatísticas
    total_doadores = len(doadores_completos)
    novos_doadores_periodo = len(novos_doadores)
    doadores_ativos = len([d for d in doadores_completos if d['status']])
    doadores_elegiveis = len([d for d in doadores_completos if d['elegivel']])
    
    # Estatísticas por tipo sanguíneo
    tipos_sanguineos = {}
    for doador in doadores_completos:
        tipo = f"{doador['tipo_sanguineo']}{doador['fator_rh']}"
        tipos_sanguineos[tipo] = tipos_sanguineos.get(tipo, 0) + 1
    
    response = templates.TemplateResponse(
        "gestor/gestor_relatorio_doador.html",
        {
            "request": request,
            "active_page": "relatorio",
            "usuario": usuario_logado,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "doadores": doadores_completos,
            "novos_doadores": novos_doadores,
            "total_doadores": total_doadores,
            "novos_doadores_periodo": novos_doadores_periodo,
            "doadores_ativos": doadores_ativos,
            "doadores_elegiveis": doadores_elegiveis,
            "tipos_sanguineos": tipos_sanguineos
        }
    )
    return response

@router.get("/gestor/relatorio/doador/pdf")
@requer_autenticacao(["gestor"])
async def get_gestor_relatorio_doador_pdf(
    data_inicio: str = Query(...),
    data_fim: str = Query(...),
    usuario_logado: dict = None
):
    # Buscar todos os doadores
    doadores = doador_repo.obter_todos()
    usuarios = usuario_repo.obter_todos()
    
    # Criar dicionário de usuários por ID
    usuarios_dict = {u.cod_usuario: u for u in usuarios}
    
    # Filtrar por período
    data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d").date()
    
    # Enriquecer doadores com dados do usuário
    novos_doadores = []
    for doador in doadores:
        usuario = usuarios_dict.get(doador.cod_doador)
        if usuario and usuario.data_cadastro and data_inicio_obj <= usuario.data_cadastro <= data_fim_obj:
            novos_doadores.append({
                'nome': usuario.nome,
                'email': usuario.email,
                'tipo_sanguineo': f"{doador.tipo_sanguineo}{doador.fator_rh}",
                'data_cadastro': usuario.data_cadastro
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
    elements.append(Paragraph("Relatório de Doadores", title_style))
    elements.append(Paragraph(f"Período: {data_inicio} a {data_fim}", styles['Normal']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Estatísticas
    elements.append(Paragraph(f"<b>Novos Doadores no Período:</b> {len(novos_doadores)}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabela de novos doadores
    if novos_doadores:
        elements.append(Paragraph("<b>Novos Doadores Cadastrados</b>", styles['Heading2']))
        data = [["Nome", "E-mail", "Tipo Sanguíneo", "Data Cadastro"]]
        for doador in novos_doadores[:50]:  # Limitar a 50
            data.append([
                doador['nome'][:30],
                doador['email'][:30],
                doador['tipo_sanguineo'],
                str(doador['data_cadastro'])
            ])
        
        table = Table(data, colWidths=[2*inch, 2*inch, 1*inch, 1.5*inch])
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
        elements.append(Paragraph("Nenhum novo doador cadastrado no período.", styles['Normal']))
    
    doc.build(elements)
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=relatorio_doadores_{data_inicio}_{data_fim}.pdf"
        }
    )