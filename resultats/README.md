# Résultats - Équipe 9 : Predict'Mob

## 📋 Contenu de ce dossier

Ce dossier contient les livrables finaux du projet **Predict'Mob** développé lors du Hackathon Mobilités 2025.

---

## 📁 Structure

```
resultats/
├── repository/                           # 💻 Code source complet
│   ├── backoffice/                      # Back-office entreprise (Streamlit)
│   ├── services/                        # Services backend, ML et mobile
│   │   ├── backend/                    # API FastAPI
│   │   ├── Mobile/                     # App Android (Kotlin)
│   │   ├── predict-delays/             # Module ML (XGBoost)
│   │   ├── migration/                  # Schéma BDD + données démo
│   │   └── database/                   # Configuration PostgreSQL
│   ├── docs/                           # Documentation technique
│   └── docker-compose.yml              # Orchestration complète
│
├── Equipe 9 - Predict'mob Final.pptx    # 📊 Présentation pitch
└── LIENS_UTILES.md                      # 🔗 Ressources et références

```

---

## 🚀 Démarrage Rapide

### Lancer le projet complet

```bash
cd repository/

# Copier la configuration
cp .env.example .env

# Démarrer tous les services
docker-compose up -d
```

**Services disponibles** :
- 🌐 Backend API : http://localhost:8000
- 🖥️ Adminer (DB) : http://localhost:9000
- 📊 Back-office : http://localhost:8501

📖 **Documentation complète** : [`repository/README.md`](repository/README.md)

---

## 📊 Présentation Finale

**Pitch du projet** : [`Equipe 9 - Predict'mob Final.pptx`](Equipe%209%20-%20Predict'mob%20Final.pptx)

Présentation de la solution finale avec :
- Problématique et proposition de valeur
- Architecture technique
- Démo des fonctionnalités
- Vision et roadmap

---

## 🔗 Liens et Ressources

Toutes les ressources, APIs, documentation et contacts sont regroupés dans :

👉 **[LIENS_UTILES.md](LIENS_UTILES.md)**

---

## 💡 Le Projet Predict'Mob

### 🎯 Proposition de Valeur

**Double levier pour une mobilité durable** :

1. **🔮 Prédiction & Alternatives** (Usagers)
   - Prédiction des retards train/RER (ML XGBoost)
   - Détection automatique des hotspots
   - Alternatives éco-responsables avec score RSE
   - Gamification (points, badges, leaderboard)

2. **📈 Indicateurs RSE** (Entreprises)
   - Dashboard CO₂ économisé
   - Taux de trajets durables
   - Engagement équipes
   - Reporting environnemental

### 🏗️ Architecture

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│  App Mobile │       │  Back-office │       │  Backend    │
│  (Android)  │◄─────►│  (Streamlit) │◄─────►│  (FastAPI)  │
└─────────────┘       └──────────────┘       └──────┬──────┘
                                                     │
                                    ┌────────────────┼────────────────┐
                                    │                │                │
                               ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐
                               │  ML     │    │ PostgreSQL│   │  Adminer  │
                               │ XGBoost │    │  + Démo   │   │  Web UI   │
                               └─────────┘    └───────────┘   └───────────┘
```

### 🛠️ Stack Technique

| Composant | Technologies |
|-----------|--------------|
| **Mobile** | Kotlin, Jetpack Compose, Material3 |
| **Backend** | FastAPI, SQLAlchemy, Pydantic |
| **ML** | XGBoost, scikit-learn, pandas |
| **Base de données** | PostgreSQL 15, Flyway |
| **Back-office** | Streamlit, plotly |
| **DevOps** | Docker, Docker Compose |

### 📊 Données Utilisées

- **PRIM** (IDFM) : Ponctualité Transilien/RER
- **GTFS/GTFS-RT** : Horaires théoriques et temps réel
- **Météo France** : Climatologie + vigilance
- **Données démo** : Intégrées dans les migrations

---

## 👥 Équipe

**Équipe 9 - Predict'Mob**

| Rôle | Membres |
|------|---------|
| **Architecture** | Sofiene, David |
| **Data Science / ML** | Marc, Marc, Stéphane |
| **Backend** | Gabriel |
| **Frontend / Mobile** | Sami |
| **UX/UI** | David, Sami, Sofiene |

---

## 📝 Documentation

### Fichiers Principaux

| Document | Description |
|----------|-------------|
| [`../README.md`](../README.md) | README principal du projet |
| [`repository/README.md`](repository/README.md) | Documentation code source |
| [`repository/docs/environement.md`](repository/docs/environement.md) | Guide Docker et environnement |
| [`repository/services/Mobile/DOCUMENTATION.md`](repository/services/Mobile/DOCUMENTATION.md) | Documentation app mobile |
| [`repository/services/backend/README.md`](repository/services/backend/README.md) | Documentation API |
| [`LIENS_UTILES.md`](LIENS_UTILES.md) | Ressources et références |

---

## 🏆 Hackathon Mobilités 2025

- **Organisation** : Île-de-France Mobilités
- **Dates** : 13-14 novembre 2025
- **Défi** : "Comment encourager les usagers à adopter des pratiques de mobilité plus durables ?"
- **Équipe** : Predict'Mob (Équipe 9)

### Liens Officiels

- **GitHub Hackathon** : https://github.com/hackathons-mobilites/hackathon_mobilites_2025
- **Branche Équipe** : https://github.com/hackathons-mobilites/hackathon_mobilites_2025/tree/equipe-9
- **PRIM API** : https://prim.iledefrance-mobilites.fr/

---

## 📄 Licence

MIT - Voir [LICENSE](../LICENSE)

---

## 🚀 Pour Aller Plus Loin

### Prochaines Étapes

1. **Intégration API temps réel** : Connexion aux flux GTFS-RT
2. **Enrichissement ML** : Plus de features (trafic, événements, travaux)
3. **Partenariats mobilité** : BlaBlacar, Vélib', opérateurs VTC électriques
4. **Gamification avancée** : Défis collectifs, récompenses partenaires
5. **Mobile iOS** : Version SwiftUI
6. **Web app** : Version navigateur responsive

### Évolutions Techniques

- ⚡ Cache Redis pour les prédictions
- 🔄 WebSockets pour notifications temps réel
- 📊 Analytics avancés (Metabase, Superset)
- 🔐 OAuth2 / OIDC pour authentification entreprise
- 🌍 Internationalisation (i18n)
- ♿ Accessibilité RGAA

---

**🎉 Merci d'avoir consulté notre projet ! N'hésitez pas à explorer le code et la documentation.**
