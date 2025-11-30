# Frontend Dockerfile - Multi-stage build
FROM node:20-alpine AS builder

# Metadados
LABEL maintainer="Financial Manager"
LABEL description="React Frontend for Financial Manager"

# Argumento para URL da API
ARG VITE_API_URL=https://financial-clever.com.br/api

# Variável de ambiente para build
ENV VITE_API_URL=$VITE_API_URL

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY package*.json ./

# Instalar dependências
RUN npm ci --only=production=false

# Copiar código fonte
COPY . .

# Build da aplicação
RUN npm run build

# Stage 2: Nginx para servir arquivos estáticos
FROM nginx:alpine

# Copiar arquivos buildados
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuração customizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]

