from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
from typing import Optional
from calendar import monthrange
from app.database import get_db
from app.models import Transaction, TransactionType, User
from app.schemas import DashboardStats, HourlyCalculationRequest, HourlyCalculationResponse
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obter estatísticas do dashboard do usuário logado"""
    # Totais respeitando filtros de data e usuário
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "income",
        Transaction.user_id == current_user.id
    )
    if start_date:
        total_income = total_income.filter(Transaction.date >= start_date)
    if end_date:
        total_income = total_income.filter(Transaction.date <= end_date)
    total_income = total_income.scalar() or 0.0
    
    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "expense",
        Transaction.user_id == current_user.id
    )
    if start_date:
        total_expense = total_expense.filter(Transaction.date >= start_date)
    if end_date:
        total_expense = total_expense.filter(Transaction.date <= end_date)
    total_expense = total_expense.scalar() or 0.0
    
    balance = total_income - total_expense
    
    # Gastos fixos
    fixed_expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "expense",
        Transaction.subtype == "fixed",
        Transaction.user_id == current_user.id
    )
    if start_date:
        fixed_expenses = fixed_expenses.filter(Transaction.date >= start_date)
    if end_date:
        fixed_expenses = fixed_expenses.filter(Transaction.date <= end_date)
    fixed_expenses = fixed_expenses.scalar() or 0.0
    
    # Gastos esporádicos
    sporadic_expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "expense",
        Transaction.subtype == "sporadic",
        Transaction.user_id == current_user.id
    )
    if start_date:
        sporadic_expenses = sporadic_expenses.filter(Transaction.date >= start_date)
    if end_date:
        sporadic_expenses = sporadic_expenses.filter(Transaction.date <= end_date)
    sporadic_expenses = sporadic_expenses.scalar() or 0.0
    
    # Investimentos
    investments = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "income",
        Transaction.subtype == "investment",
        Transaction.user_id == current_user.id
    )
    if start_date:
        investments = investments.filter(Transaction.date >= start_date)
    if end_date:
        investments = investments.filter(Transaction.date <= end_date)
    investments = investments.scalar() or 0.0
    
    # Saldo mensal (recebidos do mês atual - gastos do mês atual)
    today = date.today()
    month_start = today.replace(day=1)
    _, last_day = monthrange(today.year, today.month)
    month_end = today.replace(day=last_day)
    
    monthly_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "income",
        Transaction.user_id == current_user.id,
        Transaction.date >= month_start,
        Transaction.date <= month_end
    ).scalar() or 0.0
    
    monthly_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "expense",
        Transaction.user_id == current_user.id,
        Transaction.date >= month_start,
        Transaction.date <= month_end
    ).scalar() or 0.0
    
    monthly_balance = float(monthly_income) - float(monthly_expense)
    
    # Por categoria - Despesas
    expense_by_category = {}
    expense_query = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.type == "expense",
        Transaction.user_id == current_user.id
    )
    if start_date:
        expense_query = expense_query.filter(Transaction.date >= start_date)
    if end_date:
        expense_query = expense_query.filter(Transaction.date <= end_date)
    expenses = expense_query.group_by(Transaction.category).all()
    
    for category, total in expenses:
        expense_by_category[category or "Other"] = float(total or 0)
    
    # Por categoria - Receitas
    income_by_category = {}
    income_query = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.type == "income",
        Transaction.user_id == current_user.id
    )
    if start_date:
        income_query = income_query.filter(Transaction.date >= start_date)
    if end_date:
        income_query = income_query.filter(Transaction.date <= end_date)
    incomes = income_query.group_by(Transaction.category).all()
    
    for category, total in incomes:
        income_by_category[category or "Other"] = float(total or 0)
    
    # Tendência mensal (últimos 12 meses)
    monthly_trend = []
    for i in range(12):
        month_start = date.today().replace(day=1)
        month_start = month_start.replace(month=(month_start.month - i) % 12 or 12)
        if month_start.month > date.today().month:
            month_start = month_start.replace(year=month_start.year - 1)
        
        month_end = month_start.replace(day=28)  # Aproximação
        
        month_income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.type == "income",
            Transaction.user_id == current_user.id,
            Transaction.date >= month_start,
            Transaction.date <= month_end
        ).scalar() or 0.0
        
        month_expense = db.query(func.sum(Transaction.amount)).filter(
            Transaction.type == "expense",
            Transaction.user_id == current_user.id,
            Transaction.date >= month_start,
            Transaction.date <= month_end
        ).scalar() or 0.0
        
        monthly_trend.append({
            "month": month_start.strftime("%Y-%m"),
            "income": float(month_income),
            "expense": float(month_expense)
        })
    
    monthly_trend.reverse()
    
    # Transações recentes (respeitando filtros e usuário)
    recent_query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    if start_date:
        recent_query = recent_query.filter(Transaction.date >= start_date)
    if end_date:
        recent_query = recent_query.filter(Transaction.date <= end_date)
    recent_transactions = recent_query.order_by(
        Transaction.date.desc()
    ).limit(10).all()
    
    return DashboardStats(
        total_income=float(total_income),
        total_expense=float(total_expense),
        balance=float(balance),
        expense_by_category=expense_by_category,
        income_by_category=income_by_category,
        monthly_trend=monthly_trend,
        recent_transactions=[{
            "id": t.id,
            "type": str(t.type),
            "description": t.description,
            "amount": t.amount,
            "date": t.date.isoformat(),
            "category": t.category
        } for t in recent_transactions],
        fixed_expenses=float(fixed_expenses),
        sporadic_expenses=float(sporadic_expenses),
        investments=float(investments),
        monthly_balance=monthly_balance
    )

@router.post("/hourly-calculation", response_model=HourlyCalculationResponse)
def calculate_hourly_values(
    request: HourlyCalculationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Calcular valores por hora, dia e semana baseado em recebidos do mês"""
    # Obter primeiro e último dia do mês
    _, last_day = monthrange(request.year, request.month)
    month_start = date(request.year, request.month, 1)
    month_end = date(request.year, request.month, last_day)
    
    # Buscar total recebido no mês (subtype = "received" ou type = "income")
    total_received = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "income",
        Transaction.user_id == current_user.id,
        Transaction.date >= month_start,
        Transaction.date <= month_end
    ).scalar() or 0.0
    
    total_received = float(total_received)
    
    # Calcular valores
    total_hours = request.days_worked * request.hours_per_day
    value_per_hour = total_received / total_hours if total_hours > 0 else 0.0
    value_per_day = total_received / request.days_worked if request.days_worked > 0 else 0.0
    value_per_week = value_per_day * 7
    
    month_names = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                   "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    month_name = month_names[request.month]
    
    return HourlyCalculationResponse(
        total_received=total_received,
        days_worked=request.days_worked,
        hours_per_day=request.hours_per_day,
        total_hours=total_hours,
        value_per_hour=value_per_hour,
        value_per_day=value_per_day,
        value_per_week=value_per_week,
        month=f"{month_name}/{request.year}"
    )

