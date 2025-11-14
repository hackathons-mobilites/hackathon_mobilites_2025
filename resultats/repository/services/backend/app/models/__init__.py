"""
Modules SQLAlchemy pour PredictMob
"""
from .base import Base, TimestampMixin
from .alternative import Alternative

__all__ = ["Base", "TimestampMixin", "Alternative"]