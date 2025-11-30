from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from app.models import TransactionType

class TransactionBase(BaseModel):
    type: TransactionType
    subtype: Optional[str] = None  # fixed, sporadic, investment, received
    description: str
    amount: float = Field(gt=0)
    date: date
    category: Optional[str] = "Other"
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    subtype: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[date] = None
    category: Optional[str] = None
    notes: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_income: float
    total_expense: float
    balance: float
    expense_by_category: dict
    income_by_category: dict
    monthly_trend: list
    recent_transactions: list
    fixed_expenses: float
    sporadic_expenses: float
    investments: float
    monthly_balance: float  # Recebidos do mês - Gastos do mês

class HourlyCalculationRequest(BaseModel):
    month: int  # 1-12
    year: int
    days_worked: int
    hours_per_day: float

class HourlyCalculationResponse(BaseModel):
    total_received: float
    days_worked: int
    hours_per_day: float
    total_hours: float
    value_per_hour: float
    value_per_day: float
    value_per_week: float
    month: str

class ReportRequest(BaseModel):
    start_date: date
    end_date: date
    transaction_type: Optional[TransactionType] = None
    category: Optional[str] = None
    format: str = "pdf"  # pdf or excel

# Schemas de autenticação
class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class TokenRefresh(BaseModel):
    refresh_token: str

