# 🔒 Guia de Segurança - Financial Manager

## Implementações de Segurança

### 1. Autenticação

#### JWT Tokens
- **Access Token**: Expira em 30 minutos (configurável via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Refresh Token**: Expira em 7 dias (configurável via `REFRESH_TOKEN_EXPIRE_DAYS`)
- Tokens são armazenados no localStorage do frontend
- Refresh automático quando o access token expira
- Tokens incluem informações de role (admin/user) no payload

#### Hash de Senhas
- Usa **bcrypt** para hash de senhas
- Senhas nunca são armazenadas em texto plano
- Salt automático pelo bcrypt
- Validação de força de senha no backend

#### Política de Senha Forte
A senha deve atender aos seguintes critérios:
- ✅ Mínimo 12 caracteres
- ✅ Mínimo 2 letras maiúsculas (A-Z)
- ✅ Mínimo 2 letras minúsculas (a-z)
- ✅ Mínimo 2 números (0-9)
- ✅ Mínimo 1 caractere especial (!@#$%^&*(),.?":{}|<>)

### 2. Autorização

#### Rotas Protegidas
Todas as rotas de dados requerem autenticação:
- `/api/transactions/*` - CRUD de transações (requer autenticação)
- `/api/dashboard/*` - Estatísticas e cálculos (requer autenticação)
- `/api/reports/*` - Geração de relatórios (requer autenticação)
- `/api/upload/*` - Upload de arquivos (requer autenticação)
- `/api/users/*` - Gerenciamento de usuários (requer autenticação + role admin)

#### Rotas Públicas
- `/api/auth/login` - Login
- `/api/auth/refresh` - Renovar token
- `/api/health` - Health check

#### Rotas Removidas
- ❌ `/api/auth/register` - Registro público **REMOVIDO**
  - Apenas usuários admin podem criar novos usuários através da interface web

#### Role-Based Access Control (RBAC)
- **Admin**: Acesso completo, incluindo gerenciamento de usuários
- **User**: Acesso às funcionalidades financeiras (transações, dashboard, relatórios)

### 3. Gerenciamento de Usuários

#### Criação de Usuários
- Apenas admins podem criar novos usuários
- Interface web em `/users` (apenas visível para admins)
- Validação de senha forte obrigatória
- Validação de email e username únicos

#### Edição de Usuários
- Apenas admins podem editar usuários
- Admin não pode desativar a si mesmo
- Admin não pode remover seu próprio role de admin

#### Deleção de Usuários
- Apenas admins podem deletar usuários
- Admin não pode deletar a si mesmo

### 4. Rate Limiting

Proteção contra abuso (requer `slowapi` instalado):
- **Geral**: 60 requisições/minuto por IP (configurável via `RATE_LIMIT_PER_MINUTE`)
- **Login**: 10 tentativas/minuto por IP
- **Refresh Token**: 10 tentativas/minuto por IP
- **Logout**: 10 tentativas/minuto por IP
- **Gerenciamento de Usuários**: 5-60 tentativas/minuto por IP (dependendo da operação)

⚠️ **Nota**: Rate limiting é opcional. Se `slowapi` não estiver instalado, a aplicação funciona normalmente sem rate limiting.

### 5. Headers de Segurança

Headers HTTP de segurança implementados:
- `X-Content-Type-Options: nosniff` - Previne MIME type sniffing
- `X-Frame-Options: DENY` - Previne clickjacking
- `X-XSS-Protection: 1; mode=block` - Proteção XSS
- `Strict-Transport-Security: max-age=31536000` - Força HTTPS
- `Content-Security-Policy: default-src 'self'` - Política de conteúdo
- `Referrer-Policy: strict-origin-when-cross-origin` - Controle de referrer
- `Permissions-Policy: geolocation=(), microphone=(), camera=()` - Permissões restritas

### 6. CORS

Configurado para permitir apenas origens específicas:
- Produção: `https://financial-clever.com.br`
- Desenvolvimento: `http://localhost:5173`

Configurável via variável de ambiente `CORS_ORIGINS`.

### 7. Validação de Dados

- **Backend**: Pydantic schemas para validação de todos os inputs
- **Frontend**: Validação de formulários
- Sanitização de inputs (strip, validação de tipos)
- Validação de tipos de transação (expense/income)
- Validação de subtipos (fixed/sporadic/investment/received)

### 8. HTTPS

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

5. **Usuário Admin**: Após criar o usuário admin inicial, altere a senha padrão imediatamente.

6. **Rate Limiting**: Instale `slowapi` em produção para habilitar rate limiting:
   ```bash
   pip install slowapi
   ```

## Boas Práticas

1. ✅ Senhas devem atender à política de senha forte (12+ chars, 2 maiúsculas, 2 minúsculas, 2 números, 1 especial)
2. ✅ Use senhas fortes e únicas
3. ✅ Não compartilhe tokens
4. ✅ Faça logout ao usar computadores compartilhados
5. ✅ Mantenha o backend e frontend atualizados
6. ✅ Apenas admins devem criar novos usuários
7. ✅ Revise regularmente a lista de usuários
8. ✅ Desative usuários não utilizados

## Monitoramento

- Logs de autenticação
- Logs de rate limiting (se habilitado)
- Logs de erros de segurança
- Health checks (`/api/health`)
- Logs de criação/edição/deleção de usuários

## Checklist de Deploy

- [ ] SECRET_KEY configurado e seguro (mínimo 32 caracteres)
- [ ] HTTPS configurado
- [ ] CORS configurado corretamente
- [ ] Rate limiting ativo (instalar `slowapi`)
- [ ] Headers de segurança ativos
- [ ] Banco de dados seguro
- [ ] Logs configurados
- [ ] Backup do banco de dados
- [ ] Usuário admin criado e senha alterada
- [ ] Política de senha forte implementada
- [ ] Registro público desabilitado

## Vulnerabilidades Conhecidas

### Armazenamento de Tokens
- **Status**: Tokens armazenados no localStorage
- **Risco**: XSS pode acessar tokens
- **Mitigação**: Headers de segurança, sanitização de inputs, validação de dados
- **Melhoria Futura**: Considerar httpOnly cookies

### SQLite em Produção
- **Status**: SQLite usado por padrão
- **Risco**: Limitações de concorrência e performance
- **Mitigação**: Adequado para uso pessoal/pequeno
- **Melhoria Futura**: Migrar para PostgreSQL em produção
