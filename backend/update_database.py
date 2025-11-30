#!/usr/bin/env python3
"""
Script para atualizar o banco de dados com todas as tabelas
"""
import sys
from app.database import engine, Base
from app.models import Transaction, User, RefreshToken

def update_database():
    """Recriar todas as tabelas"""
    print("🔄 Recriando tabelas do banco de dados...")
    
    # Deletar todas as tabelas
    Base.metadata.drop_all(bind=engine)
    print("✅ Tabelas antigas removidas")
    
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas:")
    print("   - transactions (com campo 'subtype')")
    print("   - users")
    print("   - refresh_tokens")
    
    print("\n✅ Banco de dados atualizado com sucesso!")
    print("⚠️  NOTA: Todos os dados anteriores foram perdidos.")

if __name__ == "__main__":
    update_database()

