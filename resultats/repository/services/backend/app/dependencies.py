"""
Dépendances FastAPI pour l'injection de dépendances.

Ce module configure l'injection de dépendances pour les services et repositories
utilisés dans les endpoints de l'API.
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.alternative_repository import AlternativeRepository
from app.services.alternative_service import AlternativeService


# Dépendances pour les repositories
async def get_alternative_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> AlternativeRepository:
    """
    Factory pour AlternativeRepository avec session de base de données.
    
    Args:
        db: Session de base de données injectée
        
    Returns:
        Instance configurée d'AlternativeRepository
    """
    return AlternativeRepository(db)


# Dépendances pour les services
async def get_alternative_service(
    alternative_repo: Annotated[AlternativeRepository, Depends(get_alternative_repository)]
) -> AlternativeService:
    """
    Factory pour AlternativeService avec repository injecté.
    
    Args:
        alternative_repo: Repository des alternatives injecté
        
    Returns:
        Instance configurée d'AlternativeService
    """
    return AlternativeService(alternative_repo)


# Types d'annotation pour l'injection dans les routes
AlternativeServiceDep = Annotated[AlternativeService, Depends(get_alternative_service)]
AlternativeRepositoryDep = Annotated[AlternativeRepository, Depends(get_alternative_repository)]
DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


# Configuration cache pour les dépendances coûteuses (si nécessaire)
@lru_cache()
def get_settings():
    """
    Configuration mise en cache pour l'application.
    
    Returns:
        Configuration de l'application
    """
    # Pour une configuration future si nécessaire
    return {}