"""
Modèle ORM SQLAlchemy pour les alternatives de transport
"""
from sqlalchemy import Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from .base import Base, TimestampMixin


class Alternative(Base, TimestampMixin):
    """
    Modèle pour les alternatives de transport proposées pour les hotspots
    """
    __tablename__ = "alternatives"
    
    # Clé primaire
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Relation avec hotspot
    hotspot_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("hotspots.id", ondelete="CASCADE"), 
        nullable=False
    )
    
    # Informations sur l'alternative
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    offre: Mapped[str] = mapped_column(Text, nullable=False)
    partenaire: Mapped[Optional[str]] = mapped_column(String(100))
    places_disponibles: Mapped[Optional[int]] = mapped_column(Integer)
    deeplink: Mapped[Optional[str]] = mapped_column(Text)
    score_rse: Mapped[Optional[float]] = mapped_column(Float)
    
    # Relations
    # hotspot = relationship("Hotspot", back_populates="alternatives")
    
    def __repr__(self):
        return f"<Alternative(id={self.id}, type='{self.type}', partenaire='{self.partenaire}')>"