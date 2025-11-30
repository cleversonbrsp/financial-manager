#!/usr/bin/env python3
"""
Script para testar login do admin
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import User
from app.auth import verify_password, get_password_hash

def test_login():
    """Testar login do admin"""
    db = SessionLocal()
    try:
        # Buscar admin
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            print("❌ Admin não encontrado!")
            return False
        
        print(f"✅ Admin encontrado: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Hash: {admin.hashed_password[:50]}...")
        
        # Testar senha
        print("\n🔐 Testando senha 'admin'...")
        is_valid = verify_password("admin", admin.hashed_password)
        
        if is_valid:
            print("✅ Senha válida!")
            return True
        else:
            print("❌ Senha inválida!")
            print("\n🔧 Tentando recriar hash...")
            new_hash = get_password_hash("admin")
            print(f"   Novo hash: {new_hash[:50]}...")
            
            # Testar novo hash
            if verify_password("admin", new_hash):
                print("✅ Novo hash funciona!")
                print("\n🔄 Atualizando senha do admin...")
                admin.hashed_password = new_hash
                db.commit()
                print("✅ Senha atualizada!")
                return True
            else:
                print("❌ Novo hash também não funciona!")
                return False
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_login()
    sys.exit(0 if success else 1)

