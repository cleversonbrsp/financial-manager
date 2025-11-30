from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.database import get_db
from app.models import Transaction, TransactionType, User
from app.auth import get_current_active_user
import pandas as pd
from io import BytesIO

router = APIRouter()

def categorize_transaction(description: str) -> str:
    """Categorização inteligente de transações"""
    description_lower = description.lower()
    
    if any(word in description_lower for word in ["aluguel", "rent"]):
        return "Aluguel"
    elif any(word in description_lower for word in ["água", "agua", "water"]):
        return "Água"
    elif any(word in description_lower for word in ["luz", "light", "energy", "energia"]):
        return "Luz"
    elif any(word in description_lower for word in ["internet", "net"]):
        return "Internet"
    elif any(word in description_lower for word in ["das", "tax"]):
        return "DAS"
    elif any(word in description_lower for word in ["contabilidade", "accounting"]):
        return "Contabilidade"
    elif any(word in description_lower for word in ["mastercard", "credit", "cartão"]):
        return "Credit Card"
    else:
        return "Other"

@router.post("/excel")
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload e importação de planilha Excel"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be Excel format (.xlsx or .xls)")
    
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents), header=None)
        
        transactions_imported = 0
        
        # Processar SAÍDAS (colunas 0-3)
        for idx, row in df.iterrows():
            # Pular cabeçalhos
            if idx < 2:
                continue
            
            # SAÍDA (Expenses) - colunas 0-3
            destino = row.iloc[0] if pd.notna(row.iloc[0]) else None
            valor_saida = row.iloc[1] if pd.notna(row.iloc[1]) else None
            data_saida = row.iloc[2] if pd.notna(row.iloc[2]) else None
            
            if destino and pd.notna(valor_saida):
                # Converter data se necessário
                if isinstance(data_saida, datetime):
                    date_obj = data_saida.date()
                elif isinstance(data_saida, str):
                    try:
                        date_obj = datetime.strptime(data_saida, "%Y-%m-%d").date()
                    except:
                        date_obj = date.today()
                else:
                    date_obj = date.today()
                
                category = categorize_transaction(str(destino))
                
                transaction = Transaction(
                    type="expense",
                    description=str(destino),
                    amount=float(valor_saida),
                    date=date_obj,
                    category=category,
                    notes=row.iloc[3] if pd.notna(row.iloc[3]) else None
                )
                db.add(transaction)
                transactions_imported += 1
            
            # SANGRIA (Income) - colunas 5-8
            origem = row.iloc[5] if pd.notna(row.iloc[5]) else None
            valor_sangria = row.iloc[6] if pd.notna(row.iloc[6]) else None
            data_sangria = row.iloc[7] if pd.notna(row.iloc[7]) else None
            
            if origem and pd.notna(valor_sangria):
                # Converter data se necessário
                if isinstance(data_sangria, datetime):
                    date_obj = data_sangria.date()
                elif isinstance(data_sangria, str):
                    try:
                        date_obj = datetime.strptime(data_sangria, "%Y-%m-%d").date()
                    except:
                        date_obj = date.today()
                else:
                    date_obj = date.today()
                
                category = categorize_transaction(str(origem))
                
                transaction = Transaction(
                    type="income",
                    description=str(origem),
                    amount=float(valor_sangria),
                    date=date_obj,
                    category=category,
                    notes=row.iloc[8] if pd.notna(row.iloc[8]) else None
                )
                db.add(transaction)
                transactions_imported += 1
        
        db.commit()
        
        return {
            "message": f"Successfully imported {transactions_imported} transactions",
            "count": transactions_imported
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

