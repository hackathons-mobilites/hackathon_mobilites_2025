# PredictMob API Backend

API backend pour le système PredictMob de prédiction des aléas de transport et alternatives de mobilité.

## 🚀 Démarrage rapide

### Prérequis

- Python 3.8+
- pip

### Installation des dépendances

```bash
cd services/backend
pip install -r requirements.txt
```

### Démarrage de l'API

```bash
# Méthode 1: Docker compose depuis la racine
docker compose up backend -d

# Méthode 2: Uvicorn direct
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Méthode 3: Module Python
python -m app.main
```

L'API sera accessible sur `http://localhost:8000`

## 📚 Documentation

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>
- **OpenAPI JSON**: <http://localhost:8000/openapi.json>

## 🛠️ Endpoints API

### API Publique v1 (`/v1/`)

#### Système de prédiction (Levier A)

- `GET /v1/hotspots` - Liste des hotspots (zones de risque)
- `GET /v1/alternatives` - Alternatives de transport pour un trajet

#### Suivi de mobilité (Levier B)  

- `POST /v1/commute-log` - Enregistrer un trajet effectué
- `POST /v1/toggle-share-consent` - Gérer le consentement de partage
- `GET /v1/rse-report` - Indicateurs RSE d'entreprise
- `GET /v1/leaderboard` - Classements par points

### API Partenaires (`/partner/`)

- `POST /partner/alternatives` - Proposer une alternative (partenaires)

### Système

- `GET /` - Point d'entrée avec informations générales
- `GET /health` - Vérification de l'état de l'API

## 🧪 Exemples d'utilisation

### Récupérer les hotspots actifs

```bash
curl "http://localhost:8000/v1/hotspots?active_only=true"
```

### Obtenir des alternatives pour un trajet

```bash
curl "http://localhost:8000/v1/alternatives?departure_station=8775810&transport_preferences=covoiturage,velo"
```

### Enregistrer un trajet

```bash
curl -X POST "http://localhost:8000/v1/commute-log" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "date_trajet": "2025-11-14",
    "mode_final": "covoiturage",
    "co2_saved_kg": 2.5
  }'
```

### Rapport RSE d'une entreprise

```bash
curl "http://localhost:8000/v1/rse-report?company_id=1"
```

## 🏗️ Architecture

L'API est construite avec:

- **FastAPI** - Framework web moderne et rapide
- **Pydantic** - Validation et sérialisation des données
- **Uvicorn** - Serveur ASGI haute performance

### Structure du projet

```
services/backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # Point d'entrée principal
│   ├── schemas.py        # Modèles Pydantic
│   └── routers/
│       ├── __init__.py
│       ├── api_v1.py     # Routes API v1
│       └── partner_api.py # Routes API partenaires
├── requirements.txt      # Dépendances
├── run_api.py           # Script de démarrage
└── README.md           # Cette documentation
```

## 🎯 Données de démonstration

Cette version utilise des données mock pour démonstration:

### Hotspots d'exemple

- **Paris Gare du Nord**: Risque élevé 8h-10h
- **La Défense**: Risque moyen 17h30-19h30

### Alternatives d'exemple

- Covoiturage BlaBlaCar
- Vélib' stations proches
- Bus RATP avec fréquence renforcée

### Données RSE simulées

- CO2 économisé: 125.5 kg/mois
- Taux de covoiturage: 35%
- Trajets durables: 78/mois

## 🔜 Prochaines étapes

1. **Intégration base de données** - Remplacement des mocks par PostgreSQL

## 🐳 Docker

L'API peut être déployée avec Docker (configuration à venir).

## 📝 Notes de développement

- Version actuelle: **1.0.0** (MVP avec mocks)
- Compatible Python 3.8+
- API RESTful avec documentation OpenAPI
- Validation automatique des données avec Pydantic
- Gestion d'erreurs HTTP appropriée
