"""
Routes API partenaire pour PredictMob
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from app.schemas import Alternative, PartnerAlternativeCreate, Hotspot, RiskLevel

router = APIRouter(prefix="/partner")

@router.post(
    "/alternatives",
    response_model=Alternative,
    status_code=status.HTTP_201_CREATED,
    tags=["Publique - API Partenaire"],
    summary="Proposer une alternative",
    description="Permet à un partenaire de proposer une alternative pour un hotspot donné"
)
def create_partner_alternative(alternative: PartnerAlternativeCreate):
    """
    Permet à un partenaire (ex: BlaBlaCar, Vélib', RATP) de proposer 
    une alternative de transport pour un hotspot spécifique.
    
    Cette API permet l'intégration des partenaires pour enrichir 
    automatiquement les alternatives disponibles.
    """
    
    # Validation mock - vérifier que le hotspot existe
    if alternative.hotspot_id not in [1, 2]:  # Mock validation
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotspot avec l'ID {alternative.hotspot_id} non trouvé"
        )
    
    # Mock response - en réalité, on sauvegarderait en base
    response = Alternative(
        id=99,  # Mock ID
        hotspot_id=alternative.hotspot_id,
        type=alternative.type,
        offre=alternative.offre,
        partenaire=alternative.partenaire,
        places_disponibles=alternative.places_disponibles,
        deeplink=alternative.deeplink,
        score_rse=alternative.score_rse,
        created_at=datetime.now()
    )
    
    return response


@router.get(
    "/hotspots",
    tags=["Publique - API Partenaire"],
    response_model=List[Hotspot],
    summary="Récupérer les zones critiques",
    description="Permet aux partenaires de connaître les zones critiques afin de préparer leurs offres"
)
def get_partner_hotspots(
    risk_level: Optional[RiskLevel] = None,
    gare_code: Optional[str] = None,
    limit: int = 50
):
    """
    Permet aux partenaires (BlaBlaCar, Vélib', RATP, etc.) de récupérer 
    la liste des zones critiques (hotspots) pour préparer leurs offres 
    d'alternatives de transport.
    
    Les partenaires peuvent filtrer par niveau de risque et gare spécifique
    pour cibler leurs propositions d'alternatives.
    """
    
    # Mock data - hotspots critiques pour les partenaires
    mock_hotspots = [
        Hotspot(
            id=1,
            gare_code="8775810",
            gare_name="Plaisir - Grignon",
            datetime_debut=datetime(2025, 11, 14, 8, 0),
            datetime_fin=datetime(2025, 11, 14, 10, 0),
            nb_trajets_affectes=1500,
            prob_retard_max=0.85,
            prob_retard_moyenne=0.65,
            risk_level=RiskLevel.high,
            created_at=datetime.now()
        ),
        Hotspot(
            id=2,
            gare_code="8775858",
            gare_name="Paris Châtelet-Les Halles",
            datetime_debut=datetime(2025, 11, 14, 7, 30),
            datetime_fin=datetime(2025, 11, 14, 9, 30),
            nb_trajets_affectes=2200,
            prob_retard_max=0.78,
            prob_retard_moyenne=0.58,
            risk_level=RiskLevel.high,
            created_at=datetime.now()
        ),
        Hotspot(
            id=3,
            gare_code="8775801",
            gare_name="Paris Gare de Lyon",
            datetime_debut=datetime(2025, 11, 14, 17, 0),
            datetime_fin=datetime(2025, 11, 14, 19, 30),
            nb_trajets_affectes=1800,
            prob_retard_max=0.72,
            prob_retard_moyenne=0.55,
            risk_level=RiskLevel.medium,
            created_at=datetime.now()
        ),
        Hotspot(
            id=4,
            gare_code="8775840",
            gare_name="Paris Montparnasse",
            datetime_debut=datetime(2025, 11, 14, 8, 15),
            datetime_fin=datetime(2025, 11, 14, 10, 15),
            nb_trajets_affectes=900,
            prob_retard_max=0.45,
            prob_retard_moyenne=0.32,
            risk_level=RiskLevel.low,
            created_at=datetime.now()
        )
    ]
    
    # Appliquer les filtres
    filtered_hotspots = mock_hotspots
    
    if risk_level:
        filtered_hotspots = [h for h in filtered_hotspots if h.risk_level == risk_level]
    
    if gare_code:
        filtered_hotspots = [h for h in filtered_hotspots if h.gare_code == gare_code]
    
    # Appliquer la limite
    return filtered_hotspots[:limit]
