# 💰 Financial Manager

Aplicação simples de controle financeiro pessoal com interface web.

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

### 3. Acessar

- **Aplicação**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

## ✨ Funcionalidades

- Dashboard com gráficos
- Adicionar/editar/deletar transações
- Importar planilha Excel
- Gerar relatórios PDF/Excel

## 📝 Importar Planilha

O botão "Importar Excel" na sidebar aceita planilhas no formato:
- Colunas 0-3: SAÍDA (Despesas) - Destino, Valor, Data, OBS  
- Colunas 5-8: SANGRIA (Receitas) - Origem, Valor, Data, OBS

## 🗄️ Banco de Dados

SQLite criado automaticamente em `backend/financial_manager.db`
