#!/bin/bash
set -e

echo "🚀 Inicializando Financial Manager Backend..."

# Inicializar banco de dados e criar admin se necessário
echo "📦 Inicializando banco de dados..."
python3 init_db.py

# Executar comando passado como argumento
exec "$@"

