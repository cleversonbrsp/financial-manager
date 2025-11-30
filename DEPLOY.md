# Guia de Deploy - Financial Manager

## 🐳 Deploy com Docker

### Pré-requisitos

- Docker e Docker Compose instalados
- Portas 80 (frontend) e 8000 (backend) disponíveis

### Build e Executar

```bash
# Build das imagens (sem cache para garantir atualizações)
docker compose build --no-cache

# Iniciar containers em background
docker compose up -d

# Ver logs em tempo real
docker compose logs -f

# Ver logs de um serviço específico
docker compose logs -f backend
docker compose logs -f frontend
```

### Verificar status

```bash
# Status dos containers
docker compose ps

# Health checks
docker compose ps
# Deve mostrar "healthy" para ambos os serviços
```

### Parar e Remover

```bash
# Parar containers
docker compose stop

# Parar e remover containers
docker compose down

# Parar, remover containers e volumes (⚠️ apaga banco de dados)
docker compose down -v
```

### Inicialização Automática

O sistema inicializa automaticamente:
- ✅ Criação das tabelas do banco de dados
- ✅ Criação do usuário admin padrão (se não existir)
- ✅ Teste de login do admin

**Credenciais padrão:**
- Username: `admin`
- Senha: `admin`

⚠️ **IMPORTANTE**: Altere a senha após o primeiro login!

### Configuração

O `docker-compose.yml` está configurado para:
- Frontend na porta 80 (proxy nginx)
- Backend na porta 8000
- Banco de dados SQLite persistido em `./backend/data/`
- Frontend usa `/api` como baseURL (proxy nginx)

## ☸️ Deploy no Kubernetes

### Pré-requisitos

- Cluster Kubernetes configurado
- `kubectl` instalado e configurado
- Ingress Controller (nginx) instalado
- Cert-Manager instalado (para SSL/TLS)

### 1. Build das imagens

```bash
./scripts/build.sh
```

### 2. Push para registry (opcional)

Se usar um registry privado:

```bash
./scripts/push-images.sh your-registry.com v1.0.0
```

E atualize os manifests do Kubernetes com o registry correto.

### 3. Deploy no Kubernetes

```bash
./scripts/deploy-k8s.sh
```

### 4. Verificar deployment

```bash
# Ver pods
kubectl get pods -n financial-manager

# Ver services
kubectl get services -n financial-manager

# Ver ingress
kubectl get ingress -n financial-manager

# Ver logs
kubectl logs -f deployment/financial-manager-backend -n financial-manager
kubectl logs -f deployment/financial-manager-frontend -n financial-manager
```

## 🔧 Configuração do DNS

Configure o DNS `financial-clever.com.br` para apontar para o IP do Ingress Controller:

```bash
# Obter IP do Ingress
kubectl get ingress -n financial-manager
```

Configure o registro A no seu provedor de DNS apontando para esse IP.

## 🔒 SSL/TLS com Cert-Manager

O Ingress está configurado para usar Cert-Manager com Let's Encrypt. Certifique-se de que:

1. Cert-Manager está instalado no cluster
2. ClusterIssuer `letsencrypt-prod` está configurado
3. O DNS está apontando corretamente

## 📊 Monitoramento

### Health Checks

- Backend: `https://financial-clever.com.br/api/health`
- Frontend: `https://financial-clever.com.br/health`

### Escalamento

Para escalar os deployments:

```bash
kubectl scale deployment/financial-manager-backend --replicas=3 -n financial-manager
kubectl scale deployment/financial-manager-frontend --replicas=3 -n financial-manager
```

## 🔄 Atualização

### Atualizar imagens

1. Build novas imagens:
```bash
./scripts/build.sh
```

2. Atualizar deployments:
```bash
kubectl rollout restart deployment/financial-manager-backend -n financial-manager
kubectl rollout restart deployment/financial-manager-frontend -n financial-manager
```

## 🗄️ Backup do Banco de Dados

O banco de dados está em um PVC. Para fazer backup:

```bash
# Listar PVCs
kubectl get pvc -n financial-manager

# Criar backup
kubectl exec -n financial-manager deployment/financial-manager-backend -- \
  tar czf /tmp/backup.tar.gz /app/data

# Copiar backup
kubectl cp financial-manager/$(kubectl get pod -n financial-manager -l app=financial-manager-backend -o jsonpath='{.items[0].metadata.name}'):/tmp/backup.tar.gz ./backup.tar.gz
```

## 🐛 Troubleshooting

### Ver logs

```bash
# Backend
kubectl logs -f deployment/financial-manager-backend -n financial-manager

# Frontend
kubectl logs -f deployment/financial-manager-frontend -n financial-manager
```

### Descrever recursos

```bash
kubectl describe pod <pod-name> -n financial-manager
kubectl describe ingress financial-manager-ingress -n financial-manager
```

### Executar shell no pod

```bash
kubectl exec -it deployment/financial-manager-backend -n financial-manager -- /bin/bash
```

