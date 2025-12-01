from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import date, datetime
import json
from app.database import engine, Base
from app.routers import transactions, reports, dashboard, upload, auth, users
from app.middleware.security import SecurityHeadersMiddleware
from app.config import settings

# Rate limiting opcional
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    RATE_LIMITING_AVAILABLE = True
except ImportError:
    RATE_LIMITING_AVAILABLE = False
    print("⚠️  slowapi não instalado. Rate limiting desabilitado.")

# Criar tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Rate Limiter (opcional)
if RATE_LIMITING_AVAILABLE:
    limiter = Limiter(key_func=get_remote_address)
    app = FastAPI(
        title="Financial Manager API",
        description="Sistema de gestão financeira",
        version="1.0.0"
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
else:
    app = FastAPI(
        title="Financial Manager API",
        description="Sistema de gestão financeira",
        version="1.0.0"
    )

# Middleware de segurança
app.add_middleware(SecurityHeadersMiddleware)

# Função auxiliar para serializar objetos date/datetime
def serialize_for_json(obj):
    """Serializa objetos date e datetime para strings ISO format"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(serialize_for_json(item) for item in obj)
    return obj

# Handler de erros de validação
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    print(f"ERRO DE VALIDAÇÃO: {errors}")
    print(f"Body recebido: {exc.body}")
    
    # Serializar erros para garantir que objetos date/datetime sejam convertidos
    serialized_errors = serialize_for_json(errors)
    
    # Serializar body também, caso contenha objetos date/datetime
    try:
        if exc.body:
            if isinstance(exc.body, (dict, list)):
                serialized_body = serialize_for_json(exc.body)
            else:
                serialized_body = str(exc.body)
        else:
            serialized_body = None
    except Exception:
        serialized_body = str(exc.body) if exc.body else None
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": serialized_errors, "body": serialized_body},
    )

# Handler de erros gerais
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    import traceback
    error_trace = traceback.format_exc()
    print(f"ERRO GERAL: {str(exc)}")
    print(f"Traceback:\n{error_trace}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Erro interno: {str(exc)}", "traceback": error_trace},
    )

# CORS para permitir requisições do frontend
from app.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])

@app.get("/")
async def root():
    return {"message": "Financial Manager API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
