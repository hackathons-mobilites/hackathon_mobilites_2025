"""
Repositories SQLAlchemy pour PredictMob
"""
from .base import BaseRepository
from .alternative_repository import AlternativeRepository

__all__ = ["BaseRepository", "AlternativeRepository"]