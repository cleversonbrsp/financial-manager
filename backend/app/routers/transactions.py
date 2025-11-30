from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models import Transaction, TransactionType, User
from app.schemas import TransactionCreate, TransactionUpdate, Transaction as TransactionSchema
from app.auth import get_current_active_user
from app.config import settings

# Rate limiting opcional
try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    limiter = Limiter(key_func=get_remote_address)
    RATE_LIMITING_AVAILABLE = True
except ImportError:
    RATE_LIMITING_AVAILABLE = False
    limiter = None

router = APIRouter()

# Decorator de rate limiting opcional
def rate_limit(limit: str):
    if RATE_LIMITING_AVAILABLE and limiter:
        return limiter.limit(limit)
    return lambda f: f  # Retorna função sem modificação se rate limiting não disponível

@router.get("/", response_model=List[TransactionSchema])
@rate_limit(f"{settings.rate_limit_per_minute}/minute")
def get_transactions(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    transaction_type: Optional[TransactionType] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Buscar todas as transações com filtros opcionais"""
    query = db.query(Transaction)
    
    if transaction_type:
        type_value = transaction_type.value if isinstance(transaction_type, TransactionType) else str(transaction_type)
        query = query.filter(Transaction.type == type_value)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    transactions = query.order_by(desc(Transaction.date)).offset(skip).limit(limit).all()
    return transactions

@router.get("/{transaction_id}", response_model=TransactionSchema)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Buscar uma transação específica"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/", response_model=TransactionSchema)
@rate_limit(f"{settings.rate_limit_per_minute}/minute")
def create_transaction(
    request: Request,
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Criar nova transação"""
    try:
        print(f"DEBUG: Recebendo transação: {transaction.model_dump()}")
        print(f"DEBUG: Tipo recebido: {transaction.type}, Tipo do objeto: {type(transaction.type)}")
        print(f"DEBUG: Subtype recebido: {transaction.subtype}, Tipo: {type(transaction.subtype)}")
        
        # Garantir que o tipo seja uma string válida
        if isinstance(transaction.type, TransactionType):
            transaction_type_value = transaction.type.value
        else:
            transaction_type_value = str(transaction.type)
        
        # Validar que o tipo é válido
        if transaction_type_value not in ["expense", "income"]:
            raise ValueError(f"Tipo inválido: {transaction_type_value}")
        
        # Tratar subtype corretamente
        subtype_value = None
        if transaction.subtype is not None:
            if isinstance(transaction.subtype, str):
                subtype_value = transaction.subtype.strip()
                if not subtype_value:  # Se ficou vazio após strip
                    subtype_value = None
            else:
                subtype_value = str(transaction.subtype).strip() if str(transaction.subtype).strip() else None
        
        print(f"DEBUG: Subtype processado: {subtype_value}")
        print(f"DEBUG: Criando transação com: type={transaction_type_value}, subtype={subtype_value}, description={transaction.description}, amount={transaction.amount}, date={transaction.date}")
        
        db_transaction = Transaction(
            type=transaction_type_value,
            subtype=subtype_value,
            description=transaction.description.strip() if transaction.description else "",
            amount=float(transaction.amount),
            date=transaction.date,
            category=(transaction.category or "Other").strip(),
            notes=transaction.notes.strip() if transaction.notes else None
        )
        print(f"DEBUG: Objeto Transaction criado, adicionando ao banco...")
        db.add(db_transaction)
        print(f"DEBUG: Fazendo commit...")
        db.commit()
        print(f"DEBUG: Fazendo refresh...")
        db.refresh(db_transaction)
        print(f"DEBUG: Transação criada com sucesso: ID {db_transaction.id}")
        return db_transaction
    except Exception as e:
        db.rollback()
        import traceback
        error_detail = str(e)
        traceback_str = traceback.format_exc()
        print(f"ERRO ao criar transação: {error_detail}")
        print(f"Traceback completo:\n{traceback_str}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar transação: {error_detail}")

@router.put("/{transaction_id}", response_model=TransactionSchema)
@rate_limit(f"{settings.rate_limit_per_minute}/minute")
def update_transaction(
    request: Request,
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualizar transação existente"""
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    update_data = transaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/{transaction_id}")
@rate_limit(f"{settings.rate_limit_per_minute}/minute")
def delete_transaction(
    request: Request,
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Deletar transação"""
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

