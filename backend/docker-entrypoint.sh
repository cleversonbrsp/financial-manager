#!/bin/bash
set -e

echo "🚀 Inicializando Financial Manager Backend..."

# Inicializar banco de dados e criar admin se necessário
echo "📦 Inicializando banco de dados..."
python3 init_db.py

# Executar migração para adicionar user_id às transações (se necessário)
echo "🔄 Executando migração de user_id..."
python3 migrate_add_user_id.py

# Testar login do admin
echo ""
echo "🧪 Testando login do admin..."
python3 test_login.py || echo "⚠️  Teste de login falhou, mas continuando..."

# Executar comando passado como argumento
exec "$@"

