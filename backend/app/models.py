from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
import enum

class TransactionType(str, enum.Enum):
    EXPENSE = "expense"  # Saída
    INCOME = "income"    # Sangria/Entrada

class Category(str, enum.Enum):
    # Despesas
    ALUGUEL = "Aluguel"
    UTILITIES = "Utilities"  # Água, Luz, Internet
    AGUA = "Água"
    LUZ = "Luz"
    INTERNET = "Internet"
    TAX = "Tax"  # DAS, Contabilidade
    CREDIT_CARD = "Credit Card"
    CONTABILIDADE = "Contabilidade"
    DAS = "DAS"
    # Receitas
    SALARY = "Salary"
    INVESTMENT = "Investment"
    OTHER = "Other"
    # Custom
    CUSTOM = "Custom"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Associar transação ao usuário
    type = Column(String(20), nullable=False)  # expense, income
    subtype = Column(String(30), nullable=True)  # fixed, sporadic, investment, received
    description = Column(String, nullable=False)  # Destino/Origem
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String, default="Other")
    notes = Column(String, nullable=True)  # OBS
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.type}, description='{self.description}', amount={self.amount})>"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String, default="user")  # admin, user, etc
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}', role='{self.role}')>"

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_revoked = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, expires_at='{self.expires_at}')>"

