#!/usr/bin/env python3
"""
Script de inicialização do banco de dados
Cria as tabelas e o usuário admin se não existir
"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base, SessionLocal
from app.models import User, Transaction, RefreshToken
from app.auth import get_password_hash

def init_database():
    """Inicializar banco de dados e criar admin se não existir"""
    print("🔄 Inicializando banco de dados...")
    
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas/verificadas")
    
    db = SessionLocal()
    try:
        # Verificar se já existe um admin
        admin = db.query(User).filter(
            (User.username == "admin") | (User.email == "admin@financial-manager.com")
        ).first()
        
        if admin:
            print(f"✅ Usuário admin já existe: {admin.username}")
            return
        
        # Criar usuário admin
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
    init_database()

