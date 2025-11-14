"""
Service métier pour les alternatives de transport
"""
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..repositories.alternative_repository import AlternativeRepository
from ..models.alternative import Alternative


class AlternativeService:
    """Service pour la gestion des alternatives de transport"""
    
    def __init__(self, alternative_repo: AlternativeRepository):
        self.alternative_repo = alternative_repo
    
    async def get_alternatives_for_route(
        self,
        departure_station: Optional[str] = None,
        arrival_station: Optional[str] = None,
        departure_time: Optional[datetime] = None,
        transport_preferences: Optional[List[str]] = None,
        employee_id: Optional[int] = None,
        limit: int = 50
    ) -> List[Alternative]:
        """
        Récupère les alternatives recommandées pour un trajet
        
        Args:
            departure_station: Code de la gare de départ
            arrival_station: Code de la gare d'arrivée
            departure_time: Heure de départ souhaitée
            transport_preferences: Types de transport préférés
            employee_id: ID de l'employé pour personnalisation
            limit: Nombre maximum d'alternatives
        """
        
        # TODO: Pour l'instant, on récupère toutes les alternatives
        # Dans le futur, on devrait :
        # 1. Trouver les hotspots actifs sur le trajet (departure -> arrival)
        # 2. Filtrer les alternatives par ces hotspots
        
        # Récupérer les alternatives avec filtres
        alternatives = await self.alternative_repo.find_by_filters(
            transport_types=transport_preferences,
            min_places=1,  # Au moins une place disponible
            limit=limit
        )
        
        # Appliquer la logique de scoring et personnalisation
        scored_alternatives = await self._apply_scoring_logic(
            alternatives, 
            employee_id, 
            transport_preferences
        )
        
        return scored_alternatives
    
    async def get_alternatives_by_hotspots(
        self,
        hotspot_ids: List[int],
        transport_preferences: Optional[List[str]] = None,
        employee_id: Optional[int] = None
    ) -> List[Alternative]:
        """
        Récupère les alternatives pour des hotspots spécifiques
        """
        alternatives = await self.alternative_repo.find_by_filters(
            hotspot_ids=hotspot_ids,
            transport_types=transport_preferences,
            min_places=1
        )
        
        return await self._apply_scoring_logic(
            alternatives, 
            employee_id, 
            transport_preferences
        )
    
    async def get_alternatives_by_type(self, alternative_type: str) -> List[Alternative]:
        """
        Récupère toutes les alternatives d'un type donné
        """
        return await self.alternative_repo.find_by_type(alternative_type)
    
    async def get_top_alternatives(self, limit: int = 10) -> List[Alternative]:
        """
        Récupère les meilleures alternatives par score RSE
        """
        return await self.alternative_repo.get_top_alternatives_by_score(limit)
    
    async def _apply_scoring_logic(
        self,
        alternatives: List[Alternative],
        employee_id: Optional[int] = None,
        preferences: Optional[List[str]] = None
    ) -> List[Alternative]:
        """
        Applique la logique de scoring et personnalisation
        
        Pour le MVP, on se contente de trier par score RSE.
        Dans le futur, on pourrait :
        - Appliquer un boost pour les préférences de transport
        - Personnaliser selon l'historique de l'employé
        - Prendre en compte la localisation
        """
        
        # Copie pour éviter de modifier la liste originale
        scored_alternatives = alternatives.copy()
        
        # Tri par score RSE décroissant (géré par le repository)
        # Les alternatives sans score RSE sont en fin de liste
        
        # Boost des préférences de transport (bonus fictif pour le MVP)
        if preferences:
            for alt in scored_alternatives:
                if alt.type in preferences:
                    # On ne modifie pas vraiment le score en base, 
                    # c'est juste pour l'ordre d'affichage
                    pass
        
        return scored_alternatives
    
    async def create_alternative(
        self,
        hotspot_id: int,
        type: str,
        offre: str,
        partenaire: Optional[str] = None,
        places_disponibles: Optional[int] = None,
        deeplink: Optional[str] = None,
        score_rse: Optional[float] = None
    ) -> Alternative:
        """
        Crée une nouvelle alternative (pour les API partenaires)
        """
        return await self.alternative_repo.create(
            hotspot_id=hotspot_id,
            type=type,
            offre=offre,
            partenaire=partenaire,
            places_disponibles=places_disponibles,
            deeplink=deeplink,
            score_rse=score_rse
        )