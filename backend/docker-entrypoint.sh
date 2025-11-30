#!/bin/bash
set -e

echo "🚀 Inicializando Financial Manager Backend..."

# Inicializar banco de dados e criar admin se necessário
echo "📦 Inicializando banco de dados..."
python3 init_db.py

# Testar login do admin
echo ""
echo "🧪 Testando login do admin..."
python3 test_login.py || echo "⚠️  Teste de login falhou, mas continuando..."

# Executar comando passado como argumento
exec "$@"

