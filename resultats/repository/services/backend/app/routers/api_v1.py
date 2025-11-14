"""
Routes API v1 pour PredictMob
"""
from fastapi import APIRouter, Query, HTTPException, status
from typing import List, Optional
from datetime import datetime, date
from app.schemas import (
    Hotspot, Alternative, CommuteLogCreate, CommuteLogResponse,
    ToggleShareConsentRequest, ShareConsentResponse,
    CompanyRseSnapshot, LeaderboardResponse, LeaderboardEntry,
    RiskLevel, AlternativeType, TransportMode
)
from app.dependencies import AlternativeServiceDep

router = APIRouter(prefix="/v1")

# Données mock pour les hotspots (conservées car non refactorisées pour l'instant)
MOCK_HOTSPOTS = [
    {
        "id": 1,
        "gare_code": "8775810",
        "gare_name": "Plaisir - Grignon",
        "datetime_debut": datetime.fromisoformat("2025-11-14T08:00:00"),
        "datetime_fin": datetime.fromisoformat("2025-11-14T10:00:00"),
        "nb_trajets_affectes": 150,
        "prob_retard_max": 0.85,
        "prob_retard_moyenne": 0.65,
        "risk_level": "high",
        "created_at": datetime.fromisoformat("2025-11-14T07:30:00")
    },
    {
        "id": 2,
        "gare_code": "8738221",
        "gare_name": "La Défense",
        "datetime_debut": datetime.fromisoformat("2025-11-14T17:30:00"),
        "datetime_fin": datetime.fromisoformat("2025-11-14T19:30:00"),
        "nb_trajets_affectes": 85,
        "prob_retard_max": 0.65,
        "prob_retard_moyenne": 0.45,
        "risk_level": "medium",
        "created_at": datetime.fromisoformat("2025-11-14T17:00:00")
    }
]

@router.get(
    "/hotspots",
    response_model=List[Hotspot],
    tags=["Publique - Core API"],
    summary="Liste des hotspots",
    description="Récupère la liste des hotspots (zones de risque de retard) selon les critères de filtrage"
)
def get_hotspots(
    departure_station: Optional[str] = Query(None, description="Code de la gare de départ pour filtrage"),
    arrival_station: Optional[str] = Query(None, description="Code de la gare d'arrivée pour filtrage"),
    risk_level: Optional[RiskLevel] = Query(None, description="Niveau de risque pour filtrage"),
    active_only: bool = Query(True, description="Ne retourner que les hotspots actuellement actifs")
):
    """
    Retourne la liste des hotspots selon les critères de filtrage.
    
    - **departure_station**: Code de la gare de départ (optionnel)
    - **arrival_station**: Code de la gare d'arrivée (optionnel) 
    - **risk_level**: Niveau de risque (low, medium, high) (optionnel)
    - **active_only**: Si True, ne retourne que les hotspots actuellement actifs
    """
    
    hotspots = MOCK_HOTSPOTS.copy()
    now = datetime.now()
    
    # Filtrage par statut actif
    if active_only:
        hotspots = [h for h in hotspots if h["datetime_debut"] <= now <= h["datetime_fin"]]
    
    # Filtrage par gare de départ/arrivée (pour la demo, on filtre sur la gare du hotspot)
    if departure_station:
        hotspots = [h for h in hotspots if h["gare_code"] == departure_station]
    if arrival_station:
        hotspots = [h for h in hotspots if h["gare_code"] == arrival_station]
    
    # Filtrage par niveau de risque
    if risk_level:
        hotspots = [h for h in hotspots if h["risk_level"] == risk_level]
    
    return [Hotspot(**h) for h in hotspots]

@router.get(
    "/alternatives",
    response_model=List[Alternative],
    summary="Liste des alternatives",
    tags=["Privé - Core API"],
    description="Récupère les alternatives de transport pour un trajet donné et des préférences"
)
async def get_alternatives(
    alternative_service: AlternativeServiceDep,
    departure_station: Optional[str] = Query(None, description="Code de la gare de départ"),
    arrival_station: Optional[str] = Query(None, description="Code de la gare d'arrivée"),
    departure_time: Optional[datetime] = Query(None, description="Heure de départ souhaitée"),
    transport_preferences: Optional[str] = Query(None, description="Types de transport préférés (séparés par des virgules)"),
    employee_id: Optional[int] = Query(None, description="ID de l'employé pour personnalisation")
):
    """
    Retourne les alternatives de transport disponibles pour un trajet.
    
    - **departure_station**: Code de la gare de départ
    - **arrival_station**: Code de la gare d'arrivée
    - **departure_time**: Heure de départ souhaitée
    - **transport_preferences**: Types préférés (ex: "covoiturage,velo")
    - **employee_id**: ID employé pour personnalisation
    """
    
    try:
        # Conversion des préférences de transport en liste
        transport_types = None
        if transport_preferences:
            transport_types = [p.strip() for p in transport_preferences.split(",")]
        
        # Appel du service pour récupérer les alternatives
        alternatives = await alternative_service.get_alternatives_for_route(
            departure_station=departure_station,
            arrival_station=arrival_station,
            departure_time=departure_time,
            transport_preferences=transport_types,
            employee_id=employee_id
        )
        
        # Conversion en schémas Pydantic pour la réponse API
        return [Alternative.model_validate(alt.__dict__) for alt in alternatives]
        
    except Exception as e:
        # Log de l'erreur et retour d'une erreur HTTP appropriée
        print(f"Erreur lors de la récupération des alternatives: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération des alternatives"
        )

@router.post(
    "/commute-log",
    response_model=CommuteLogResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Privé - Core API"],
    summary="Enregistrer un trajet",
    description="Enregistre un trajet effectué par un employé avec l'alternative choisie"
)
def create_commute_log(commute_log: CommuteLogCreate):
    """
    Enregistre un nouveau trajet effectué par un employé.
    
    Permet de tracker les choix de mobilité et calculer les impacts RSE.
    """
    
    # Mock response - en réalité, on sauvegarderait en base
    response = CommuteLogResponse(
        id=1,  # Mock ID
        employee_id=commute_log.employee_id,
        trajectory_id=commute_log.trajectory_id,
        hotspot_id=commute_log.hotspot_id,
        alternative_id=commute_log.alternative_id,
        date_trajet=commute_log.date_trajet,
        mode_final=commute_log.mode_final,
        co2_saved_kg=commute_log.co2_saved_kg,
        created_at=datetime.now()
    )
    
    return response

@router.post(
    "/toggle-share-consent",
    tags=["Privé - Core API"],
    response_model=ShareConsentResponse,
    summary="Modifier le consentement de partage",
    description="Met à jour le consentement d'un employé pour le partage de ses données avec son entreprise"
)
def toggle_share_consent(request: ToggleShareConsentRequest):
    """
    Active ou désactive le partage des données de mobilité avec l'entreprise.
    
    Respecte le RGPD en permettant à l'employé de contrôler ses données.
    """
    
    # Mock response - en réalité, on mettrait à jour la base
    response = ShareConsentResponse(
        employee_id=request.employee_id,
        share_enabled=request.share_enabled,
        updated_at=datetime.now()
    )
    
    return response

@router.get(
    "/rse-report",
    response_model=List[CompanyRseSnapshot],
    tags=["Privé - Core API"],
    summary="Rapport RSE",
    description="Récupère les indicateurs RSE d'une entreprise pour les périodes demandées"
)
def get_rse_report(
    company_id: int = Query(..., description="ID de l'entreprise"),
    period_start: Optional[str] = Query(None, description="Période de début (format YYYY-MM)"),
    period_end: Optional[str] = Query(None, description="Période de fin (format YYYY-MM)")
):
    """
    Retourne les indicateurs RSE pour une entreprise.
    
    - **company_id**: ID de l'entreprise
    - **period_start**: Période de début au format YYYY-MM
    - **period_end**: Période de fin au format YYYY-MM
    """
    
    # Mock data
    mock_snapshots = [
        {
            "id": 1,
            "company_id": company_id,
            "period": "2025-11",
            "co2_total_saved_kg": 125.5,
            "nb_trajets_partages": 45,
            "nb_trajets_durables": 78,
            "covoiturage_rate": 0.35,
            "created_at": datetime.fromisoformat("2025-11-01T00:00:00")
        },
        {
            "id": 2,
            "company_id": company_id,
            "period": "2025-10",
            "co2_total_saved_kg": 98.2,
            "nb_trajets_partages": 38,
            "nb_trajets_durables": 62,
            "covoiturage_rate": 0.28,
            "created_at": datetime.fromisoformat("2025-10-01T00:00:00")
        }
    ]
    
    # Filtrage par période
    snapshots = mock_snapshots
    if period_start:
        snapshots = [s for s in snapshots if s["period"] >= period_start]
    if period_end:
        snapshots = [s for s in snapshots if s["period"] <= period_end]
    
    return [CompanyRseSnapshot(**s) for s in snapshots]

@router.get(
    "/leaderboard",
    response_model=LeaderboardResponse,
    tags=["Privé - Core API"],
    summary="Classements internes",
    description="Récupère les classements des employés par points (entreprise et équipe)"
)
def get_leaderboard(
    company_id: int = Query(..., description="ID de l'entreprise"),
    team_id: Optional[int] = Query(None, description="ID de l'équipe (optionnel)"),
    period: Optional[str] = Query(None, description="Période (format YYYY-MM)"),
    limit: int = Query(10, description="Nombre max d'entrées dans le classement")
):
    """
    Retourne les classements par points pour motiver les employés.
    
    - **company_id**: ID de l'entreprise
    - **team_id**: ID de l'équipe (optionnel pour le classement d'équipe)
    - **period**: Période au format YYYY-MM
    - **limit**: Nombre maximum d'entrées à retourner
    """
    
    # Mock data pour le classement entreprise
    company_leaderboard = [
        LeaderboardEntry(
            employee_id=1,
            employee_name="Marie Dupont",
            total_points=1250,
            rank=1
        ),
        LeaderboardEntry(
            employee_id=2,
            employee_name="Pierre Martin",
            total_points=980,
            rank=2
        ),
        LeaderboardEntry(
            employee_id=3,
            employee_name="Sophie Chen",
            total_points=875,
            rank=3
        )
    ]
    
    # Mock data pour le classement équipe (si demandé)
    team_leaderboard = None
    if team_id:
        team_leaderboard = [
            LeaderboardEntry(
                employee_id=1,
                employee_name="Marie Dupont",
                total_points=1250,
                rank=1
            ),
            LeaderboardEntry(
                employee_id=4,
                employee_name="Thomas Dubois",
                total_points=720,
                rank=2
            )
        ]
    
    # Appliquer la limite
    company_leaderboard = company_leaderboard[:limit]
    if team_leaderboard:
        team_leaderboard = team_leaderboard[:limit]
    
    return LeaderboardResponse(
        company_leaderboard=company_leaderboard,
        team_leaderboard=team_leaderboard
    )
