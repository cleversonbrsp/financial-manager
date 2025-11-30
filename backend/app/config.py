"""
Configurações da aplicação
"""
import os
from typing import List

# Fallback para pydantic-settings se não estiver disponível
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./financial_manager.db")
    
    # CORS - converter string para lista
    cors_origins_str: str = os.getenv("CORS_ORIGINS", "https://financial-clever.com.br,http://localhost:5173")
    
    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins_str.split(",")]
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # API
    api_title: str = "Financial Manager API"
    api_version: str = "1.0.0"
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-min-32-chars")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # Rate Limiting
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

