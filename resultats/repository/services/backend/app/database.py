"""
Configuration et gestion de la base de données PostgreSQL.

Ce module configure SQLAlchemy avec PostgreSQL et fournit
les sessions de base de données pour l'application.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config import get_database_url


# URL de connexion à la base de données
DATABASE_URL = get_database_url()

# Moteur SQLAlchemy async
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Mettre à True pour voir les requêtes SQL en debug
    future=True,
    pool_pre_ping=True,  # Vérification de la connexion avant usage
    pool_recycle=3600,  # Recyclage des connexions après 1h
)

# Factory pour les sessions
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base pour les modèles ORM
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Générateur de session de base de données pour l'injection de dépendances FastAPI.
    
    Yields:
        AsyncSession: Session de base de données configurée
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialise la base de données en créant toutes les tables.
    
    NOTE: En production, utilisez plutôt Alembic pour les migrations.
    """
    async with engine.begin() as conn:
        # Import des modèles pour s'assurer qu'ils sont enregistrés
        from app.models import alternative  # noqa
        
        # Création des tables (uniquement en développement)
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Ferme proprement les connexions à la base de données.
    """
    await engine.dispose()


# Fonction utilitaire pour vérifier la connexion
async def check_db_connection() -> bool:
    """
    Vérifie si la connexion à la base de données fonctionne.
    
    Returns:
        bool: True si la connexion réussit, False sinon
    """
    try:
        async with AsyncSessionLocal() as session:
            # Test simple avec une requête SQL littérale
            from sqlalchemy import text
            await session.execute(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return False