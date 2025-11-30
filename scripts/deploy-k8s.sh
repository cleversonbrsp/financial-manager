#!/bin/bash
# Script para deploy no Kubernetes

set -e

echo "🚀 Deploying to Kubernetes..."

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se kubectl está instalado
if ! command -v kubectl &> /dev/null; then
    echo -e "${YELLOW}❌ kubectl não encontrado. Por favor, instale o kubectl.${NC}"
    exit 1
fi

# Aplicar namespace
echo -e "${BLUE}📝 Creating namespace...${NC}"
kubectl apply -f k8s/namespace.yaml

# Aplicar PVC
echo -e "${BLUE}💾 Creating PersistentVolumeClaim...${NC}"
kubectl apply -f k8s/backend-pvc.yaml

# Aplicar backend
echo -e "${BLUE}🔧 Deploying backend...${NC}"
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml

# Aplicar frontend
echo -e "${BLUE}🎨 Deploying frontend...${NC}"
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

# Aplicar Ingress
echo -e "${BLUE}🌐 Deploying Ingress...${NC}"
kubectl apply -f k8s/ingress.yaml

echo -e "${GREEN}✅ Deployment completed!${NC}"
echo ""
echo "Verificando status..."
kubectl get pods -n financial-manager
kubectl get services -n financial-manager
kubectl get ingress -n financial-manager

