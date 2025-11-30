# 🔒 Guia de Segurança - Financial Manager

## Implementações de Segurança

### 1. Autenticação

#### JWT Tokens
- **Access Token**: Expira em 30 minutos (configurável)
- **Refresh Token**: Expira em 7 dias (configurável)
- Tokens são armazenados no localStorage do frontend
- Refresh automático quando o access token expira

#### Hash de Senhas
- Usa **bcrypt** para hash de senhas
- Senhas nunca são armazenadas em texto plano
- Salt automático pelo bcrypt

### 2. Autorização

#### Rotas Protegidas
Todas as rotas de dados requerem autenticação:
- `/api/transactions/*` - CRUD de transações
- `/api/dashboard/*` - Estatísticas e cálculos
- `/api/reports/*` - Geração de relatórios
- `/api/upload/*` - Upload de arquivos

#### Rotas Públicas
- `/api/auth/register` - Registro de usuário
- `/api/auth/login` - Login
- `/api/auth/refresh` - Renovar token
- `/api/health` - Health check

### 3. Rate Limiting

Proteção contra abuso:
- **Geral**: 60 requisições/minuto por IP
- **Login**: 10 tentativas/minuto por IP
- **Registro**: 5 tentativas/minuto por IP

### 4. Headers de Segurança

Headers HTTP de segurança implementados:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`
- `Content-Security-Policy: default-src 'self'`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: geolocation=(), microphone=(), camera=()`

### 5. CORS

Configurado para permitir apenas origens específicas:
- Produção: `https://financial-clever.com.br`
- Desenvolvimento: `http://localhost:5173`

### 6. Validação de Dados

- **Backend**: Pydantic schemas para validação
- **Frontend**: Validação de formulários
- Sanitização de inputs

### 7. HTTPS

- Configurado no Kubernetes Ingress
- Certificado SSL/TLS via Cert-Manager (Let's Encrypt)
- Redirecionamento automático HTTP → HTTPS

## Configuração de Produção

### Variáveis de Ambiente

```bash
# Backend
SECRET_KEY=your-secret-key-min-32-characters-change-this
DATABASE_URL=sqlite:///./financial_manager.db
CORS_ORIGINS=https://financial-clever.com.br
ENVIRONMENT=production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
RATE_LIMIT_PER_MINUTE=60

# Frontend
VITE_API_URL=https://financial-clever.com.br/api
```

### ⚠️ IMPORTANTE

1. **SECRET_KEY**: Mude o SECRET_KEY em produção! Use um gerador seguro:
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

2. **Banco de Dados**: Em produção, considere usar PostgreSQL em vez de SQLite para melhor performance e segurança.

3. **HTTPS**: Sempre use HTTPS em produção. Nunca envie tokens via HTTP.

4. **Tokens**: Tokens são armazenados no localStorage. Para maior segurança, considere usar httpOnly cookies.

## Boas Práticas

1. ✅ Senhas devem ter no mínimo 6 caracteres
2. ✅ Use senhas fortes e únicas
3. ✅ Não compartilhe tokens
4. ✅ Faça logout ao usar computadores compartilhados
5. ✅ Mantenha o backend e frontend atualizados

## Monitoramento

- Logs de autenticação
- Logs de rate limiting
- Logs de erros de segurança
- Health checks

## Checklist de Deploy

- [ ] SECRET_KEY configurado e seguro
- [ ] HTTPS configurado
- [ ] CORS configurado corretamente
- [ ] Rate limiting ativo
- [ ] Headers de segurança ativos
- [ ] Banco de dados seguro
- [ ] Logs configurados
- [ ] Backup do banco de dados

