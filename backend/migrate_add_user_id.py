#!/usr/bin/env python3
"""
Script de migração para adicionar campo user_id às transações existentes.
Transações existentes serão associadas ao primeiro usuário admin encontrado.
"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models import Transaction, User
from sqlalchemy import text, inspect

def migrate_add_user_id():
    """Adicionar coluna user_id à tabela transactions e associar transações existentes ao admin"""
    db = SessionLocal()
    try:
        print("🔄 Iniciando migração: adicionar user_id às transações...")
        
        # Verificar se a coluna já existe usando PRAGMA table_info (SQLite)
        try:
            result = db.execute(text("PRAGMA table_info(transactions)"))
            columns = [row[1] for row in result.fetchall()]  # row[1] é o nome da coluna
            
            if 'user_id' in columns:
                print("✅ Coluna user_id já existe. Verificando transações sem user_id...")
            else:
                print("📝 Adicionando coluna user_id à tabela transactions...")
                # Adicionar coluna user_id (permitir NULL temporariamente)
                db.execute(text("ALTER TABLE transactions ADD COLUMN user_id INTEGER"))
                db.commit()
                print("✅ Coluna user_id adicionada")
        except Exception as e:
            # Se falhar, tentar adicionar a coluna mesmo assim (pode já existir)
            print(f"⚠️  Verificação de coluna falhou: {str(e)}")
            print("📝 Tentando adicionar coluna user_id...")
            try:
                db.execute(text("ALTER TABLE transactions ADD COLUMN user_id INTEGER"))
                db.commit()
                print("✅ Coluna user_id adicionada")
            except Exception as add_error:
                # Se falhar ao adicionar, provavelmente já existe
                error_msg = str(add_error).lower()
                if "duplicate column" in error_msg or "already exists" in error_msg or "duplicate" in error_msg:
                    print("✅ Coluna user_id já existe")
                else:
                    # Se for outro erro, relançar
                    raise add_error
        
        # Buscar o primeiro usuário admin (ou primeiro usuário se não houver admin)
        admin_user = db.query(User).filter(
            (User.role == "admin") | (User.is_superuser == True)
        ).first()
        
        if not admin_user:
            # Se não houver admin, buscar o primeiro usuário
            admin_user = db.query(User).first()
        
        if not admin_user:
            print("⚠️  Nenhum usuário encontrado. Criando usuário admin padrão...")
            from app.auth import get_password_hash
            admin_user = User(
                email="admin@financial-manager.com",
                username="admin",
                hashed_password=get_password_hash("admin"),
                full_name="Administrador",
                is_active=True,
                is_superuser=True,
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"✅ Usuário admin criado: {admin_user.username} (ID: {admin_user.id})")
        else:
            print(f"✅ Usuário encontrado: {admin_user.username} (ID: {admin_user.id})")
        
        # Contar transações sem user_id
        transactions_without_user = db.query(Transaction).filter(
            Transaction.user_id == None
        ).count()
        
        if transactions_without_user > 0:
            print(f"📊 Encontradas {transactions_without_user} transações sem user_id")
            print(f"🔗 Associando transações ao usuário {admin_user.username} (ID: {admin_user.id})...")
            
            # Atualizar todas as transações sem user_id
            db.execute(text(
                "UPDATE transactions SET user_id = :user_id WHERE user_id IS NULL"
            ), {"user_id": admin_user.id})
            db.commit()
            
            print(f"✅ {transactions_without_user} transações associadas ao usuário {admin_user.username}")
        else:
            print("✅ Todas as transações já possuem user_id")
        
        # Verificar se todas as transações têm user_id
        remaining = db.query(Transaction).filter(Transaction.user_id == None).count()
        if remaining == 0:
            print("✅ Todas as transações possuem user_id associado")
        else:
            print(f"⚠️  Ainda existem {remaining} transações sem user_id")
        
        print("✅ Migração concluída com sucesso!")
        print("")
        print("📝 Nota: SQLite não suporta ALTER COLUMN para tornar NOT NULL diretamente.")
        print("   A coluna user_id foi adicionada e todas as transações foram associadas.")
        print("   Novas transações sempre terão user_id (garantido pelo código).")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro durante a migração: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    migrate_add_user_id()

