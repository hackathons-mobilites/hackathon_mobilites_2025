"""
Repository pour les alternatives de transport
"""
from typing import List, Optional
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from ..models.alternative import Alternative
from .base import BaseRepository


class AlternativeRepository(BaseRepository[Alternative]):
    """Repository pour les alternatives de transport"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, Alternative)
    
    async def find_by_hotspot_ids(self, hotspot_ids: List[int]) -> List[Alternative]:
        """Récupère les alternatives pour une liste d'hotspots"""
        if not hotspot_ids:
            return []
            
        query = select(Alternative).where(Alternative.hotspot_id.in_(hotspot_ids))
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def find_by_type(self, alternative_type: str) -> List[Alternative]:
        """Récupère les alternatives par type (covoiturage, velo, etc.)"""
        query = select(Alternative).where(Alternative.type == alternative_type)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def find_by_filters(
        self,
        hotspot_ids: Optional[List[int]] = None,
        transport_types: Optional[List[str]] = None,
        min_places: Optional[int] = None,
        min_score_rse: Optional[float] = None,
        partenaire: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Alternative]:
        """
        Récupère les alternatives avec filtres avancés
        """
        query = select(Alternative)
        conditions = []
        
        # Filtrer par hotspots
        if hotspot_ids:
            conditions.append(Alternative.hotspot_id.in_(hotspot_ids))
        
        # Filtrer par types de transport
        if transport_types:
            conditions.append(Alternative.type.in_(transport_types))
        
        # Filtrer par nombre de places disponibles
        if min_places is not None:
            conditions.append(
                and_(
                    Alternative.places_disponibles.isnot(None),
                    Alternative.places_disponibles >= min_places
                )
            )
        
        # Filtrer par score RSE minimum
        if min_score_rse is not None:
            conditions.append(
                and_(
                    Alternative.score_rse.isnot(None),
                    Alternative.score_rse >= min_score_rse
                )
            )
        
        # Filtrer par partenaire
        if partenaire:
            conditions.append(Alternative.partenaire.ilike(f"%{partenaire}%"))
        
        # Appliquer les conditions
        if conditions:
            query = query.where(and_(*conditions))
        
        # Tri par score RSE décroissant par défaut
        query = query.order_by(Alternative.score_rse.desc().nulls_last())
        
        # Limitation du nombre de résultats
        if limit:
            query = query.limit(limit)
        
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_top_alternatives_by_score(self, limit: int = 10) -> List[Alternative]:
        """Récupère les meilleures alternatives par score RSE"""
        query = (
            select(Alternative)
            .where(Alternative.score_rse.isnot(None))
            .order_by(Alternative.score_rse.desc())
            .limit(limit)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())