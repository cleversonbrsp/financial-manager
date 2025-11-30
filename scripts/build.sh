#!/bin/bash
# Script para build das imagens Docker

set -e

echo "🏗️  Building Docker images..."

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Build backend
echo -e "${BLUE}📦 Building backend image...${NC}"
cd backend
docker build -t financial-manager-backend:latest .
cd ..

# Build frontend
echo -e "${BLUE}📦 Building frontend image...${NC}"
cd frontend
docker build -t financial-manager-frontend:latest .
cd ..

echo -e "${GREEN}✅ Build completed successfully!${NC}"
echo ""
echo "Images created:"
echo "  - financial-manager-backend:latest"
echo "  - financial-manager-frontend:latest"

