#!/usr/bin/env python3
"""
Script para limpar todos os usuários e criar usuário admin padrão
"""
import sys
from app.database import engine, Base, SessionLocal
from app.models import User
from app.auth import get_password_hash

def create_admin():
    """Limpar usuários e criar admin"""
    db = SessionLocal()
    
    try:
        print("🗑️  Removendo todos os usuários existentes...")
        db.query(User).delete()
        db.commit()
        print("✅ Usuários removidos")
        
        print("\n👤 Criando usuário admin padrão...")
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
        
        print("✅ Usuário admin criado com sucesso!")
        print(f"\n📋 Credenciais:")
        print(f"   Email: admin@financial-manager.com")
        print(f"   Username: admin")
        print(f"   Senha: admin")
        print(f"\n⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()

