# Predict'Mob — Code Source et Services

Ce dossier contient l'ensemble du code source du projet Predict'Mob développé lors du Hackathon Mobilités 2025.

## 📁 Structure du projet

```
repository/
├── backoffice/              # Back-office Entreprise (Streamlit)
├── services/                # Services backend et ML
│   ├── backend/            # API FastAPI
│   ├── database/           # Configuration PostgreSQL
│   ├── migration/          # Migrations Flyway (schéma v3)
│   └── predict-delays/     # Module ML de prédiction (XGBoost)
├── docker-compose.yml       # Orchestration complète
└── docker-compose.build.yml # Build des images Docker
```

---

## 🚀 Démarrage rapide

### Prérequis

- Docker & Docker Compose 20+
- Python 3.11+ (pour développement local)

### Lancer tous les services

```bash
cd resultats/repository/
docker-compose up -d
```

Cela démarre :
- 🗄️ **PostgreSQL** (port 5432) - Base de données
- ⚡ **Backend API** (port 8000) - FastAPI
- 📊 **Back-office** (port 8501) - Streamlit
- 🤖 **Module Predict** - Service de prédiction ML

### Accéder aux services

| Service | URL | Description |
|---------|-----|-------------|
| API Backend | http://localhost:8000 | API REST (doc: `/docs`) |
| Back-office | http://localhost:8501 | Dashboard entreprise |
| PostgreSQL | localhost:5432 | BDD (user: `predictmob`) |

---

## 📦 Composants

### 1️⃣ Backend API (`services/backend/`)

API REST FastAPI avec :
- **Levier A** : `/v1/hotspots`, `/v1/alternatives`
- **Levier B** : `/v1/commute-log`, `/v1/rse-report`, `/v1/leaderboard`
- **Partenaires** : `/partner/alternatives`

**Technologies** : FastAPI, Pydantic, Uvicorn

📖 [Documentation complète](services/backend/README.md)

### 2️⃣ Module ML Predict (`services/predict-delays/`)

Modèle de prédiction des retards train/RER :
- **Algorithme** : XGBoost Regressor
- **Données** : PRIM (Transilien) + Météo France
- **Target** : Délai additionnel à l'arrivée (minutes)
- **Features** : Ligne, station, horaire, météo, historique

📖 [Documentation ML](services/predict-delays/README.md)

### 3️⃣ Base de données (`services/migration/`)

Schéma PostgreSQL v3 avec :
- Tables entreprises : `companies`, `company_sites`, `employees`
- Tables prédiction : `trajectories`, `predictions`, `hotspots`
- Tables mobilité : `alternatives`, `commute_logs`, `mobility_events`
- Tables gamification : `rewards`, `employee_points`
- Tables RSE : `employee_settings`, `company_rse_snapshot`

**Migration** : Flyway (versionnée)

### 4️⃣ Back-office Entreprise (`backoffice/`)

Interface Streamlit pour :
- **Onboarding** : Import Excel ou connecteur LDAP
- **Dashboard RSE** : Métriques CO₂, covoiturage, trajets durables
- **Hotspots** : Alertes en temps réel
- **Leaderboard** : Classements gamifiés

📖 [Documentation back-office](backoffice/README.md)

---

## 🔧 Développement local

### Backend API

```bash
cd services/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Back-office

```bash
cd backoffice
pip install -r requirements.txt
streamlit run app.py
```

### Module Predict

```bash
cd services/predict-delays
pip install -r requirements.txt
python train/model_building/train_model.py
```

---

## 🗄️ Base de données

### Connexion

```bash
psql -h localhost -p 5432 -U predictmob -d predictmob
```

### Appliquer les migrations

```bash
docker-compose up migration
```

### Schéma

Le schéma complet v3 se trouve dans :
`services/migration/migrations/versioned/V1__predictmob_schema_v3.sql`

---

## 🧪 Tests

### Tester l'API

```bash
# Health check
curl http://localhost:8000/health

# Hotspots
curl http://localhost:8000/v1/hotspots

# Alternatives
curl "http://localhost:8000/v1/alternatives?departure_station=8775810"

# Rapport RSE
curl "http://localhost:8000/v1/rse-report?company_id=1"
```

---

## 📊 Données

### Sources

- **PRIM** (IDFM) : Ponctualité Transilien/RER
- **GTFS/GTFS-RT** : Horaires théoriques et temps réel
- **Météo France** : Climatologie horaire + vigilance
- **SIRENE** (INSEE) : Référentiel entreprises

### Format

Les données sont accessibles via :
- Datalab Onyxia (pendant le hackathon)
- APIs PRIM (production)

---

## 🐳 Docker

### Build des images

```bash
docker-compose -f docker-compose.build.yml build
```

### Logs

```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f backend
```

### Arrêter

```bash
docker-compose down
```

### Reset complet

```bash
docker-compose down -v  # Supprime aussi les volumes
```

---

## 🔐 Variables d'environnement

Créer un fichier `.env` à la racine :

```env
# Database
POSTGRES_USER=predictmob
POSTGRES_PASSWORD=hackathon2025
POSTGRES_DB=predictmob
DATABASE_URL=postgresql://predictmob:hackathon2025@database:5432/predictmob

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# API Keys (optionnel)
PRIM_API_KEY=your_key
METEO_API_KEY=your_key

# Streamlit
STREAMLIT_SERVER_PORT=8501
BACKEND_API_URL=http://backend:8000
```

---

## 📝 Architecture technique

```
┌─────────────────────────────────────────────────────────┐
│                     UTILISATEURS                         │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
    ┌────────▼──────────┐      ┌─────────▼──────────┐
    │  App Mobile Web   │      │   Back-office      │
    │  (HTML/CSS/JS)    │      │   (Streamlit)      │
    └────────┬──────────┘      └─────────┬──────────┘
             │                            │
             └────────────┬───────────────┘
                          │
                 ┌────────▼─────────┐
                 │   Backend API    │
                 │   (FastAPI)      │
                 │                  │
                 │  /v1/hotspots    │
                 │  /v1/alternatives│
                 │  /v1/rse-report  │
                 └────────┬─────────┘
                          │
      ┌───────────────────┼───────────────────┐
      │                   │                   │
 ┌────▼────┐      ┌──────▼──────┐     ┌─────▼─────┐
 │ Module  │      │  PostgreSQL │     │   APIs    │
 │ Predict │      │     v15     │     │ Externes  │
 │ XGBoost │      │             │     │           │
 │         │      │ - companies │     │ - PRIM    │
 └─────────┘      │ - employees │     │ - GTFS-RT │
                  │ - hotspots  │     │ - Météo   │
                  │ - mobility  │     └───────────┘
                  └─────────────┘
```

---

## 🤝 Contribution

### Équipe Predict'Mob - Hackathon Mobilités 2025

- **Architecture** : Sofiene, David
- **Data Science** : Marc, Marc, Stéphane
- **Backend** : Gabriel
- **Frontend** : Sami
- **UX/UI** : David, Sami, Sofiene

---

## 📄 Licence

MIT - Voir [LICENSE](../../LICENSE)

---

## 🔗 Liens utiles

- [README principal du projet](../../README.md)
- [Documentation Hackathon Mobilités 2025](https://github.com/hackathons-mobilites/hackathon_mobilites_2025)
- [API PRIM](https://prim.iledefrance-mobilites.fr/)

