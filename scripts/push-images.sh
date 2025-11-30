#!/bin/bash
# Script para fazer push das imagens para registry

set -e

REGISTRY=${1:-"your-registry.com"}
VERSION=${2:-"latest"}

echo "📤 Pushing images to registry: $REGISTRY"

# Tag images
docker tag financial-manager-backend:latest $REGISTRY/financial-manager-backend:$VERSION
docker tag financial-manager-frontend:latest $REGISTRY/financial-manager-frontend:$VERSION

# Push images
docker push $REGISTRY/financial-manager-backend:$VERSION
docker push $REGISTRY/financial-manager-frontend:$VERSION

echo "✅ Images pushed successfully!"

