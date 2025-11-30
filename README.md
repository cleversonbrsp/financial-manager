# 💰 Financial Manager

Sistema completo de gestão financeira pessoal com interface web moderna, autenticação segura e gerenciamento de usuários.

## 🚀 Executar

⚠️ **IMPORTANTE**: Você precisa ter DOIS terminais abertos - um para backend e outro para frontend!

### 1. Backend (Terminal 1)

```bash
cd backend
pip3 install -r requirements.txt
python3 -m uvicorn app.main:app --reload --port 8000
```

Você deve ver: `Uvicorn running on http://127.0.0.1:8000`

### 2. Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

Você deve ver: `Local: http://localhost:5173/`

### 3. Inicializar Admin

Na primeira execução, crie o usuário admin padrão:

```bash
cd backend
python3 create_admin.py
```

**Credenciais padrão:**
- Username: `admin`
- Email: `admin@financial-manager.com`
- Senha: `AdminPassword@123`

⚠️ **IMPORTANTE**: Altere a senha após o primeiro login!

### 4. Acessar

- **Aplicação**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Login**: http://localhost:5173/login

## ✨ Funcionalidades

### 📊 Dashboard
- Estatísticas financeiras em tempo real
- Gráficos de tendências mensais
- Gráficos de categorias (receitas e despesas)
- Transações recentes
- Cálculo de saldo mensal
- Cálculo de valor por hora/dia/semana

### 💳 Transações
- Adicionar/editar/deletar transações
- Tipos: Receita (income) e Despesa (expense)
- Subtipos: Fixos, Esporádicos, Investimentos, Recebidos
- Categorização automática
- Importar planilha Excel
- Filtros e busca

### 📄 Relatórios
- Gerar relatórios PDF
- Gerar relatórios Excel
- Filtros por período, tipo e categoria

### 👥 Gerenciamento de Usuários (Admin)
- Criar novos usuários
- Editar usuários existentes
- Deletar usuários
- Atribuir roles (admin/user)
- Ativar/desativar usuários

### 🔐 Autenticação
- Login seguro com JWT
- Refresh token automático
- Proteção de rotas
- Validação de senha forte
- Role-based access control (RBAC)

## 📝 Importar Planilha

O botão "Importar Excel" na sidebar aceita planilhas no formato:
- Colunas 0-3: SAÍDA (Despesas) - Destino, Valor, Data, OBS  
- Colunas 5-8: SANGRIA (Receitas) - Origem, Valor, Data, OBS

## 🗄️ Banco de Dados

SQLite criado automaticamente em `backend/financial_manager.db`

### Estrutura

- **transactions**: Transações financeiras
- **users**: Usuários do sistema
- **refresh_tokens**: Tokens de refresh para autenticação

## 🔒 Segurança

### Política de Senha
- Mínimo 12 caracteres
- Mínimo 2 letras maiúsculas
- Mínimo 2 letras minúsculas
- Mínimo 2 números
- Mínimo 1 caractere especial

### Autenticação
- JWT tokens (access + refresh)
- Bcrypt para hash de senhas
- Rate limiting (opcional, requer `slowapi`)
- Headers de segurança HTTP
- CORS configurado

### Autorização
- Rotas protegidas por autenticação
- Rotas admin protegidas por role
- Registro público desabilitado (apenas admin cria usuários)

Veja [SECURITY.md](SECURITY.md) para mais detalhes.

## 📱 PWA (Progressive Web App)

A aplicação é compatível com instalação em dispositivos móveis Android:
- Service Worker para cache offline
- Manifest para instalação
- Interface responsiva

## 🐳 Deploy com Docker

### Executar com Docker Compose

```bash
# Build e iniciar containers
docker compose build --no-cache
docker compose up -d

# Ver logs
docker compose logs -f

# Parar containers
docker compose down
```

### Acessar após deploy

- **Aplicação**: http://localhost
- **API Docs**: http://localhost:8000/docs
- **Login**: http://localhost/login

**Credenciais padrão após primeira inicialização:**
- Username: `admin`
- Senha: `admin`

⚠️ **IMPORTANTE**: Altere a senha do admin após o primeiro login!

### Notas sobre Docker

- O banco de dados é inicializado automaticamente na primeira execução
- O usuário admin é criado automaticamente se não existir
- O banco de dados é persistido em `./backend/data/`
- O frontend usa proxy nginx para `/api` → backend na porta 8000

Veja [DEPLOY.md](DEPLOY.md) para instruções detalhadas de deploy com Docker e Kubernetes.

## 🛠️ Tecnologias

### Backend
- FastAPI
- SQLAlchemy (ORM)
- SQLite
- JWT (python-jose)
- Bcrypt (passlib)
- Pandas (processamento de dados)
- ReportLab (PDF)

### Frontend
- React 18 + TypeScript
- Vite
- TailwindCSS
- Recharts (gráficos)
- React Router
- Axios

## 📚 Documentação

- [SECURITY.md](SECURITY.md) - Guia de segurança
- [DEPLOY.md](DEPLOY.md) - Guia de deploy

## 🐛 Troubleshooting

### Backend não inicia
- Verifique se a porta 8000 está livre
- Verifique se todas as dependências estão instaladas: `pip3 install -r requirements.txt`

### Frontend não conecta ao backend
- Verifique se o backend está rodando na porta 8000
- Verifique o arquivo `.env` ou variáveis de ambiente

### Erro de autenticação
- Verifique se o usuário admin foi criado: `python3 create_admin.py`
- Verifique se o token não expirou (faça login novamente)

## 📄 Licença

Este projeto é de uso pessoal.
