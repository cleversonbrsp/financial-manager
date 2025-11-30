from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from app.database import get_db
from app.models import Transaction, TransactionType, User
from app.auth import get_current_active_user, User
from app.auth import get_current_active_user
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

router = APIRouter()

@router.get("/pdf")
def generate_pdf_report(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    transaction_type: Optional[TransactionType] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Gerar relatório em PDF do usuário logado"""
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if transaction_type:
        type_value = transaction_type.value if isinstance(transaction_type, TransactionType) else str(transaction_type)
        query = query.filter(Transaction.type == type_value)
    if category:
        query = query.filter(Transaction.category == category)
    
    transactions = query.order_by(Transaction.date.desc()).all()
    
    # Calcular totais
    total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
    total_expense = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
    balance = total_income - total_expense
    
    # Criar PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Título
    elements.append(Paragraph("Relatório Financeiro", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Período
    period_text = f"Período: {start_date or 'Início'} a {end_date or 'Hoje'}"
    elements.append(Paragraph(period_text, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumo
    summary_data = [
        ['Resumo Financeiro', '', ''],
        ['Receitas', f'R$ {total_income:,.2f}', ''],
        ['Despesas', f'R$ {total_expense:,.2f}', ''],
        ['Saldo', f'R$ {balance:,.2f}', '']
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Transações
    if transactions:
        elements.append(Paragraph("Transações", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        trans_data = [['Data', 'Tipo', 'Descrição', 'Categoria', 'Valor']]
        
        for t in transactions:
            trans_data.append([
                t.date.strftime("%d/%m/%Y"),
                "Receita" if t.type == TransactionType.INCOME else "Despesa",
                t.description,
                t.category or "Outro",
                f"R$ {t.amount:,.2f}"
            ])
        
        trans_table = Table(trans_data, colWidths=[1*inch, 1*inch, 2.5*inch, 1.5*inch, 1.5*inch])
        trans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(trans_table)
    
    # Gerar PDF
    doc.build(elements)
    buffer.seek(0)
    
    return StreamingResponse(
        BytesIO(buffer.read()),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=relatorio_financeiro.pdf"}
    )

@router.get("/excel")
def generate_excel_report(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    transaction_type: Optional[TransactionType] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Gerar relatório em Excel do usuário logado"""
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if transaction_type:
        type_value = transaction_type.value if isinstance(transaction_type, TransactionType) else str(transaction_type)
        query = query.filter(Transaction.type == type_value)
    if category:
        query = query.filter(Transaction.category == category)
    
    transactions = query.order_by(Transaction.date.desc()).all()
    
    # Preparar dados
    data = []
    for t in transactions:
        data.append({
            "Data": t.date.strftime("%d/%m/%Y"),
            "Tipo": "Receita" if t.type == TransactionType.INCOME else "Despesa",
            "Descrição": t.description,
            "Categoria": t.category or "Outro",
            "Valor": t.amount,
            "Observações": t.notes or ""
        })
    
    df = pd.DataFrame(data)
    
    # Criar Excel com formatação
    output = BytesIO()
    try:
        from openpyxl.styles import Font, PatternFill, Alignment
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Transações', index=False)
            
            # Formatação
            workbook = writer.book
            worksheet = writer.sheets['Transações']
            
            # Cabeçalho
            header_fill = PatternFill(start_color="6366F1", end_color="6366F1", fill_type="solid")
            header_font = Font(color="FFFFFF", bold=True)
            
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")
            
            # Ajustar largura das colunas
            worksheet.column_dimensions['A'].width = 12
            worksheet.column_dimensions['B'].width = 12
            worksheet.column_dimensions['C'].width = 30
            worksheet.column_dimensions['D'].width = 15
            worksheet.column_dimensions['E'].width = 15
            worksheet.column_dimensions['F'].width = 30
    except ImportError:
        # Fallback se openpyxl não estiver disponível
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Transações', index=False)
    
    output.seek(0)
    
    return StreamingResponse(
        BytesIO(output.read()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=relatorio_financeiro.xlsx"}
    )

