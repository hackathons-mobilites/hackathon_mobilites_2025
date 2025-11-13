# Back-office Entreprise - Predict'Mob

Interface Streamlit pour les entreprises permettant de gérer l'onboarding des salariés et visualiser les indicateurs RSE.

## Fonctionnalités

### 🚀 Onboarding Entreprise
- Création d'entreprise (nom, SIREN, secteur)
- Ajout de sites
- Import Excel des salariés
- Template Excel fourni

### 📊 Dashboard RSE
- Métriques clés : CO₂ évité, taux de covoiturage, trajets durables
- Graphiques d'évolution CO₂
- Répartition des modes de transport
- Export de rapports (à venir)

### ⚠️ Hotspots
- Visualisation des zones à risque en temps réel
- Nombre de salariés impactés
- Niveaux de criticité (élevé, moyen, faible)

### 🏆 Leaderboard
- Classement des équipes
- Podium mensuel
- Points et badges de gamification

## Installation

```bash
cd backoffice
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

L'application sera accessible sur http://localhost:8501

## Structure

```
backoffice/
├── app.py                      # Application principale + onboarding
├── pages/
│   ├── 1_📊_Dashboard_RSE.py   # Métriques RSE détaillées
│   ├── 2_⚠️_Hotspots.py        # Alertes en temps réel
│   └── 3_🏆_Leaderboard.py     # Classements
├── data/
│   └── mock_data.py            # Données fictives pour démo
└── requirements.txt
```

## Données fictives

Cette version utilise des données fictives (mock) pour la démonstration.
Pour connecter à l'API backend réelle, modifier `data/mock_data.py` pour appeler les endpoints FastAPI.

## Note

Version prototype pour le Hackathon Mobilités 2025.
RGPD compliant : seuls les salariés ayant activé le partage opt-in contribuent aux métriques RSE.

