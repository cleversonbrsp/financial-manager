#!/bin/bash
# Script para iniciar o backend usando Python do sistema (não do Cursor)

echo "🚀 Iniciando backend FastAPI na porta 8000..."
echo "📝 Usando Python do sistema: /usr/bin/python3"
echo ""

# Usar Python do sistema explicitamente
/usr/bin/python3 -m uvicorn app.main:app --reload --port 8000

