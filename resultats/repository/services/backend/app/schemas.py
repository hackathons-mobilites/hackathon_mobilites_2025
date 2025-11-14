"""
Modèles Pydantic pour les API de PredictMob
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

# Enums
class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TransportMode(str, Enum):
    train = "train"
    metro = "metro"
    bus = "bus"
    velo = "velo"
    covoiturage = "covoiturage"
    marche = "marche"
    trottinette = "trottinette"

class AlternativeType(str, Enum):
    covoiturage = "covoiturage"
    velo = "velo"
    transport_public = "transport_public"
    marche = "marche"
    trottinette = "trottinette"

# Modèles pour les hotspots
class Hotspot(BaseModel):
    id: int = Field(..., description="ID unique du hotspot")
    gare_code: str = Field(..., description="Code de la gare concernée")
    gare_name: str = Field(..., description="Nom de la gare")
    datetime_debut: datetime = Field(..., description="Début de la période de risque")
    datetime_fin: datetime = Field(..., description="Fin de la période de risque")
    nb_trajets_affectes: int = Field(..., description="Nombre de trajets potentiellement affectés")
    prob_retard_max: float = Field(..., description="Probabilité de retard maximale", ge=0, le=1)
    prob_retard_moyenne: Optional[float] = Field(None, description="Probabilité de retard moyenne", ge=0, le=1)
    risk_level: RiskLevel = Field(..., description="Niveau de risque")
    created_at: datetime = Field(..., description="Date de création")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "gare_code": "8775810",
                "gare_name": "Paris Gare du Nord",
                "datetime_debut": "2025-11-14T08:00:00Z",
                "datetime_fin": "2025-11-14T10:00:00Z",
                "nb_trajets_affectes": 150,
                "prob_retard_max": 0.85,
                "prob_retard_moyenne": 0.65,
                "risk_level": "high",
                "created_at": "2025-11-14T07:30:00Z"
            }
        }

# Modèles pour les alternatives
class Alternative(BaseModel):
    id: int = Field(..., description="ID unique de l'alternative")
    hotspot_id: int = Field(..., description="ID du hotspot associé")
    type: AlternativeType = Field(..., description="Type d'alternative")
    offre: str = Field(..., description="Description de l'offre")
    partenaire: Optional[str] = Field(None, description="Nom du partenaire proposant l'alternative")
    places_disponibles: Optional[int] = Field(None, description="Nombre de places disponibles")
    deeplink: Optional[str] = Field(None, description="Lien vers l'application du partenaire")
    score_rse: Optional[float] = Field(None, description="Score RSE de l'alternative", ge=0, le=10)
    created_at: datetime = Field(..., description="Date de création")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "hotspot_id": 1,
                "type": "covoiturage",
                "offre": "Covoiturage Paris Nord - La Défense, départ 8h15",
                "partenaire": "BlaBlaCar",
                "places_disponibles": 3,
                "deeplink": "https://blablacar.com/ride/12345",
                "score_rse": 8.5,
                "created_at": "2025-11-14T07:45:00Z"
            }
        }

# Modèles pour les logs de trajets
class CommuteLogCreate(BaseModel):
    employee_id: int = Field(..., description="ID de l'employé")
    trajectory_id: Optional[int] = Field(None, description="ID du trajet habituel")
    hotspot_id: Optional[int] = Field(None, description="ID du hotspot rencontré")
    alternative_id: Optional[int] = Field(None, description="ID de l'alternative choisie")
    date_trajet: date = Field(..., description="Date du trajet")
    mode_final: Optional[TransportMode] = Field(None, description="Mode de transport final utilisé")
    co2_saved_kg: Optional[float] = Field(None, description="CO2 économisé en kg", ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 1,
                "trajectory_id": 1,
                "hotspot_id": 1,
                "alternative_id": 1,
                "date_trajet": "2025-11-14",
                "mode_final": "covoiturage",
                "co2_saved_kg": 2.5
            }
        }

class CommuteLogResponse(BaseModel):
    id: int = Field(..., description="ID unique du log")
    employee_id: int = Field(..., description="ID de l'employé")
    trajectory_id: Optional[int] = Field(None, description="ID du trajet habituel")
    hotspot_id: Optional[int] = Field(None, description="ID du hotspot rencontré")
    alternative_id: Optional[int] = Field(None, description="ID de l'alternative choisie")
    date_trajet: date = Field(..., description="Date du trajet")
    mode_final: Optional[TransportMode] = Field(None, description="Mode de transport final utilisé")
    co2_saved_kg: Optional[float] = Field(None, description="CO2 économisé en kg")
    created_at: datetime = Field(..., description="Date de création")

# Modèles pour le consentement de partage
class ToggleShareConsentRequest(BaseModel):
    employee_id: int = Field(..., description="ID de l'employé")
    share_enabled: bool = Field(..., description="Autoriser le partage des données avec l'entreprise")

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 1,
                "share_enabled": True
            }
        }

class ShareConsentResponse(BaseModel):
    employee_id: int = Field(..., description="ID de l'employé")
    share_enabled: bool = Field(..., description="Statut du partage")
    updated_at: datetime = Field(..., description="Date de mise à jour")

# Modèles pour les rapports RSE
class CompanyRseSnapshot(BaseModel):
    id: int = Field(..., description="ID unique du snapshot")
    company_id: int = Field(..., description="ID de l'entreprise")
    period: str = Field(..., description="Période du rapport (ex: '2025-11')")
    co2_total_saved_kg: Optional[float] = Field(None, description="Total CO2 économisé en kg")
    nb_trajets_partages: Optional[int] = Field(None, description="Nombre de trajets en mobilité partagée")
    nb_trajets_durables: Optional[int] = Field(None, description="Nombre de trajets en mobilité durable")
    covoiturage_rate: Optional[float] = Field(None, description="Taux de covoiturage", ge=0, le=1)
    created_at: datetime = Field(..., description="Date de création")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "company_id": 1,
                "period": "2025-11",
                "co2_total_saved_kg": 125.5,
                "nb_trajets_partages": 45,
                "nb_trajets_durables": 78,
                "covoiturage_rate": 0.35,
                "created_at": "2025-11-01T00:00:00Z"
            }
        }

# Modèles pour les leaderboards
class LeaderboardEntry(BaseModel):
    employee_id: int = Field(..., description="ID de l'employé")
    employee_name: str = Field(..., description="Nom de l'employé")
    total_points: int = Field(..., description="Total des points")
    rank: int = Field(..., description="Classement")

class LeaderboardResponse(BaseModel):
    company_leaderboard: List[LeaderboardEntry] = Field(..., description="Classement de l'entreprise")
    team_leaderboard: Optional[List[LeaderboardEntry]] = Field(None, description="Classement de l'équipe (optionnel)")

    class Config:
        json_schema_extra = {
            "example": {
                "company_leaderboard": [
                    {
                        "employee_id": 1,
                        "employee_name": "Marie Dupont",
                        "total_points": 1250,
                        "rank": 1
                    },
                    {
                        "employee_id": 2,
                        "employee_name": "Pierre Martin",
                        "total_points": 980,
                        "rank": 2
                    }
                ],
                "team_leaderboard": [
                    {
                        "employee_id": 1,
                        "employee_name": "Marie Dupont",
                        "total_points": 1250,
                        "rank": 1
                    }
                ]
            }
        }

# Modèles pour les alternatives des partenaires
class PartnerAlternativeCreate(BaseModel):
    hotspot_id: int = Field(..., description="ID du hotspot concerné")
    type: AlternativeType = Field(..., description="Type d'alternative")
    offre: str = Field(..., description="Description de l'offre")
    partenaire: str = Field(..., description="Nom du partenaire")
    places_disponibles: Optional[int] = Field(None, description="Nombre de places disponibles")
    deeplink: Optional[str] = Field(None, description="Lien vers l'application du partenaire")
    score_rse: Optional[float] = Field(None, description="Score RSE de l'alternative", ge=0, le=10)

    class Config:
        json_schema_extra = {
            "example": {
                "hotspot_id": 1,
                "type": "velo",
                "offre": "Vélib' disponible à 200m de la gare",
                "partenaire": "Vélib'",
                "places_disponibles": 5,
                "deeplink": "https://velib-metropole.fr/map",
                "score_rse": 9.0
            }
        }