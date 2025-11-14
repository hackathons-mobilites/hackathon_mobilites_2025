"""
Configuration de l'application PredictMob.

Ce module contient les paramètres de configuration pour la base de données,
l'API et les autres services.
"""

import os
from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseModel):
    """Configuration de la base de données PostgreSQL."""
    
    host: str = "db"
    port: int = 5432
    username: str = "postgres"
    password: str = "postgres"
    database: str = "predictmob"
    
    @property
    def url(self) -> str:
        """URL de connexion PostgreSQL pour SQLAlchemy."""
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def sync_url(self) -> str:
        """URL de connexion synchrone pour les migrations."""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class APISettings(BaseModel):
    """Configuration de l'API FastAPI."""
    
    title: str = "PredictMob API"
    description: str = "API pour la prédiction et gestion de la mobilité"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    """Configuration principale de l'application."""
    
    # Configuration base de données
    database: DatabaseSettings = DatabaseSettings()
    
    # Configuration API
    api: APISettings = APISettings()
    
    # Variables d'environnement spécifiques
    environment: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = False


# Instance globale des paramètres
settings = Settings()


def get_settings() -> Settings:
    """
    Factory pour récupérer la configuration de l'application.
    
    Returns:
        Instance de la configuration
    """
    return settings


# Configuration par environnement
def get_database_url() -> str:
    """
    Récupère l'URL de la base de données selon l'environnement.
    
    Returns:
        URL de connexion à la base de données
    """
    # En production, on utilisera les variables d'environnement
    if settings.environment == "production":
        return os.getenv("DATABASE_URL", settings.database.url)
    
    # En développement, on utilise la configuration par défaut
    return settings.database.url


def get_database_sync_url() -> str:
    """
    Récupère l'URL synchrone de la base de données pour les migrations.
    
    Returns:
        URL de connexion synchrone
    """
    if settings.environment == "production":
        sync_url = os.getenv("DATABASE_SYNC_URL")
        if sync_url:
            return sync_url
    
    return settings.database.sync_url