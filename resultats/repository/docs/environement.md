# Documentation PredictMob

## 🐳 Architecture Docker et Lancement de la Stack

### Vue d'ensemble

L'application PredictMob est containerisée avec Docker Compose et organisée en plusieurs services indépendants :

```
┌─────────────────┐    ┌─────────────────┐    ┌───────────────────────────────────┐
│    Frontend     │    │    Backend      │    │   PostgreSQL                      │
│   (à venir)     │◄──►│   FastAPI       │◄──►│   Database                        │
│                 │    │   Port: 8000    │    │   Port: 5432                      │
└─────────────────┘    └─────────────────┘    └───────────────────────────────────┘
                                                        ▲              ▲         ▲
                                                        │              │         │
                                               ┌─────────────────┐     │         │
                                               │    Adminer      │     │         │
                                               │   Interface DB  │     │         │
                                               │   Port: 9000    │     │         │
                                               └─────────────────┘     │         │
                                                                       │         │
                                                              ┌────────┴────┐    │
                                                              │  Migration  │    │
                                                              │   Flyway    │    │
                                                              │ (One-time)  │    │
                                                              └─────────────┘    │
                                                                                 │
                                                                    ┌────────────┴────────────┐
                                                                    │    Predict-Delays       │
                                                                    │     ML Model            │
                                                                    │     XGBoost             │
                                                                    │ (Données IDFM +         │
                                                                    │  Météo France)          │
                                                                    └─────────────────────────┘
```

### 🧠 Modèle de Prédiction des Retards

Le service **Predict-Delays** utilise un modèle XGBoost pour prédire les retards de transport :

- **Sources de données** :
  - Données historiques IDFM (horaires Transilien)
  - Prévisions météorologiques Météo France
  - Alertes météo
- **Cible** : `Delais_additionnel_a_l_arrivee` (retard supplémentaire en minutes)
- **Pipeline** : Préprocessing + XGBoost Regressor
- **Intégration** : Stockage des prédictions dans PostgreSQL pour génération des hotspots

### 🔄 Flux de Données et Intégration ML (Entrainement)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Données   │    │   Modèle    │    │ PostgreSQL  │    │   Backend   │
│   IDFM +    │───►│  XGBoost    │───►│  Database   │───►│   FastAPI   │
│ Météo France│    │ Prédiction  │    │ Stockage    │    │  Hotspots   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Processus de prédiction et intégration :**

1. **Collecte des données** : Récupération des données historiques IDFM et météorologiques
2. **Entraînement** : Modèle XGBoost entraîné sur `Delais_additionnel_a_l_arrivee`
3. **Prédiction temps réel** : Génération de prédictions de retards pour les prochaines heures
4. **Stockage direct DB** : Insertion directe des prédictions dans PostgreSQL (tables `predictions` et `hotspots`)
5. **Exposition API** : Backend FastAPI expose les hotspots via `/v1/hotspots`
6. **Alternatives** : Génération automatique d'alternatives pour les hotspots détectés

### 🚀 Lancement rapide de la stack

#### Prérequis

- Docker et Docker Compose installés
- Fichier `.env` configuré (voir exemple ci-dessous)

#### Commandes de base

```bash
# 1. Démarrer tous les services
docker compose up -d

# 2. Vérifier l'état des services
docker compose ps

# 3. Voir les logs
docker compose logs -f

# 4. Arrêter la stack
docker compose down

# 5. Arrêter et supprimer les volumes (⚠️ perte de données)
docker compose down -v
```

#### Lancement par étapes

```bash
# 1. Base de données uniquement
docker compose up -d db

# 2. Appliquer les migrations
docker compose run --rm migration migrate

# 3. Démarrer le backend
docker compose up -d backend

# 4. Interface d'administration (optionnel)
docker compose up -d adminer
```

### 📋 Composants Docker

#### 🗄️ **Database (PostgreSQL 15)**

- **Service** : `db`
- **Image** : `postgres:15`
- **Port** : `5432` (configurable via `POSTGRES_SERVICE_PORT`)
- **Responsabilités** :
  - Stockage des données applicatives (hotspots, alternatives, utilisateurs)
  - Persistance via volume Docker `db_data`
  - Configuration via variables d'environnement

#### 🔄 **Migration (Flyway)**

- **Service** : `migration` / `migration-init`
- **Image** : `flyway/flyway:latest`
- **Responsabilités** :
  - Application automatique des migrations de schéma
  - Gestion des versions de base de données
  - Exécution des scripts SQL versionnés et répétables
  - Validation de la cohérence des migrations

#### 🚀 **Backend (FastAPI)**

- **Service** : `backend`
- **Image** : `python:3.11-slim`
- **Port** : `8000` (configurable via `BACKEND_SERVICE_PORT`)
- **Responsabilités** :
  - API REST pour l'application mobile et web
  - Endpoints `/v1/alternatives`, `/v1/hotspots`, etc.
  - Logique métier et accès aux données
  - Documentation API automatique (Swagger/ReDoc)

#### 🧠 **Predict-Delays (Modèle ML)**

- **Service** : `predict-delays` (en développement)
- **Technologie** : Python + XGBoost + scikit-learn
- **Type** : Service batch de prédiction
- **Dialogue direct avec** : PostgreSQL Database (pas via API Backend)
- **Responsabilités** :
  - Entraînement du modèle XGBoost sur données historiques IDFM
  - Prédiction des retards avec météorologie (Météo France)
  - Génération des hotspots de risque en temps réel
  - **Stockage direct** : Insertion directe dans PostgreSQL (connexion DB dédiée)
  - Pipeline de preprocessing automatisé
- **Sources de données** :
  - Données transiliennes SNCF (horaires théoriques vs réalisés)
  - Prévisions météorologiques horaires
  - Alertes vigilance météo
- **Cible** : Prédiction `Delais_additionnel_a_l_arrivee` (minutes de retard)

#### 🖥️ **Adminer (Interface DB)**

- **Service** : `adminer`
- **Image** : `adminer:latest`
- **Port** : `9000` (configurable via `ADMINER_SERVICE_PORT`)
- **Responsabilités** :
  - Interface web pour l'administration PostgreSQL
  - Visualisation et modification des données
  - Exécution de requêtes SQL
  - Gestion des tables et structures

### 🔗 URLs d'accès

Une fois la stack démarrée :

| Service | URL | Description |
|---------|-----|-------------|
| **API Backend** | <http://localhost:8000> | API REST principale |
| **Documentation API** | <http://localhost:8000/docs> | Swagger UI |
| **ReDoc API** | <http://localhost:8000/redoc> | Documentation alternative |
| **Health Check** | <http://localhost:8000/health> | Vérification santé API |
| **Hotspots (Prédictions)** | <http://localhost:8000/v1/hotspots> | Zones de retard prédites par ML |
| **Alternatives** | <http://localhost:8000/v1/alternatives> | Solutions de mobilité alternative |
| **Adminer** | <http://localhost:9000> | Interface administration DB |

### 🐛 Dépannage

```bash
# Voir les logs d'un service spécifique
docker compose logs backend
docker compose logs db

# Redémarrer un service
docker compose restart backend

# Reconstruire un service (après modification)
docker compose build backend
docker compose up -d backend

# Accéder au shell d'un conteneur
docker compose exec backend bash
docker compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB
```

---

## Variables d'environnement

### PostgreSQL

| Variable                | Description                                           | Valeur par défaut |
|-------------------------|------------------------------------------------------|-------------------|
| `POSTGRES_SERVICE_PORT` | Port d'écoute du service PostgreSQL                  | 5432              |
| `POSTGRES_DB`           | Nom de la base de données utilisée par l'application | predictmob        |
| `POSTGRES_USER`         | Nom d'utilisateur pour la connexion PostgreSQL       | predictmob        |
| `POSTGRES_PASSWORD`     | Mot de passe de l'utilisateur PostgreSQL             | predictmob_pwd    |

### Backend API

| Variable               | Description                           | Valeur par défaut |
|------------------------|---------------------------------------|-------------------|
| `BACKEND_SERVICE_PORT` | Port d'écoute du service Backend API  | 8000              |
| `API_DEBUG`            | Mode debug de l'API (true/false)      | false             |
| `API_LOG_LEVEL`        | Niveau de logs (INFO, DEBUG, ERROR)   | INFO              |

### Adminer

| Variable               | Description                           | Valeur par défaut |
|------------------------|---------------------------------------|-------------------|
| `ADMINER_SERVICE_PORT` | Port d'écoute du service Adminer      | 9000              |

---

## Guide de migration (Flyway)

Les migrations de base de données sont gérées avec l'outil **Flyway**.

### Commandes principales

| Commande   | Description                                      |
|------------|--------------------------------------------------|
| `info`     | Affiche l'état des migrations                    |
| `migrate`  | Applique les migrations non encore exécutées     |
| `clean`    | Supprime toutes les tables de la base de données |
| `validate` | Vérifie la cohérence des migrations              |

#### Exemple d'utilisation

```bash
docker compose run --rm migration <commande>
```

Remplacez `<commande>` par l'une des commandes listées ci-dessus.

---

### Création de migrations

Pour créer une migration, ajoutez un fichier SQL dans le dossier de migrations monté dans le conteneur Flyway (par exemple `./migrations`).

Flyway distingue deux types de migrations :

- **Migrations versionnées** : utilisées pour les évolutions du schéma (création/modification de tables, etc.).
  - Format de nom attendu : `V<version>__<description>.sql`
  - Exemple : `V1__init_schema.sql`, `V2__ajout_table_utilisateur.sql`

- **Migrations répétables** : utilisées pour des scripts à réappliquer à chaque changement (vues, fonctions, données de référence, etc.).
  - Format de nom attendu : `R__<description>.sql`
  - Exemple : `R__vues_metier.sql`, `R__data_reference.sql`

Placez les fichiers dans les sous-dossiers `versioned` ou `repeatable` selon la configuration de votre service Flyway.

Lors de l'exécution de la commande `migrate`, Flyway applique automatiquement les migrations versionnées non encore exécutées et réapplique les migrations répétables si leur contenu a changé.

> **Remarque importante sur les migrations répétables** :
>
> Les scripts de migration répétables doivent pouvoir être réexécutés à tout moment sans provoquer de duplication de données ou d'erreurs. Pour cela, il est recommandé d'utiliser des clauses comme `ON CONFLICT` lors des insertions (`INSERT ... ON CONFLICT DO NOTHING`), ou d'adopter une stratégie de suppression préalable des données concernées (`DELETE FROM ...` suivi d'un `INSERT`).
>
> Exemple :
>
> ```sql
> INSERT INTO reference_table (id, label) VALUES (1, 'valeur')
>   ON CONFLICT (id) DO UPDATE SET label = EXCLUDED.label;
> ```
>
> ou
>
> ```sql
> DELETE FROM reference_table;
> INSERT INTO reference_table (id, label) VALUES (1, 'valeur');
> ```

---

### Exemple de configuration `.env`

```env
# Configuration PostgreSQL
POSTGRES_SERVICE_PORT=5432
POSTGRES_DB=predictmob
POSTGRES_USER=predictmob
POSTGRES_PASSWORD=predictmob_pwd

# Configuration Backend API
BACKEND_SERVICE_PORT=8000
API_DEBUG=false
API_LOG_LEVEL=INFO

# Configuration Adminer
ADMINER_SERVICE_PORT=9000

# Configuration pour le développement local (optionnel)
# DATABASE_URL=postgresql://predictmob:predictmob_pwd@localhost:5432/predictmob
```

### 🚀 Démarrage rapide avec .env

1. **Créer le fichier .env** à la racine du projet avec la configuration ci-dessus
2. **Démarrer la stack complète** :

   ```bash
   docker compose up -d
   ```

3. **Vérifier que tout fonctionne** :

   ```bash
   # Vérifier les services
   docker compose ps
   
   # Tester l'API
   curl http://localhost:8000/health
   
   # Tester une requête d'alternatives
   curl http://localhost:8000/v1/alternatives
   ```

---

## 🧪 Tests et Développement

### Chargement des données de test

Pour tester l'API avec des données réalistes :

```bash
# 1. Copier le fichier .env.example
cp .env.example .env

# 2. Démarrer PostgreSQL et appliquer les migrations
docker compose up -d db
docker compose run --rm migration migrate

# 3. Charger les données de test
cd services/backend
psql postgresql://predictmob:predictmob_pwd@localhost:5432/predictmob -f test_data.sql

# 4. Démarrer l'API
docker compose up -d backend
```

---

## Accès à Adminer

Adminer est une interface web permettant de gérer la base de données PostgreSQL facilement.

Après avoir démarré les services avec :

```bash
docker compose up -d
```

Accédez à Adminer via votre navigateur à l’adresse suivante :

```
http://localhost:9000
```

(Remplacez `9000` par la valeur de la variable `ADMINER_SERVICE_PORT` si vous l’avez modifiée dans votre fichier `.env`.)

- Système : `PostgreSQL`
- Serveur : `db` (ou laissez la valeur par défaut si déjà renseignée)
- Utilisateur : la valeur de `POSTGRES_USER`
- Mot de passe : la valeur de `POSTGRES_PASSWORD`
- Base de données : la valeur de `POSTGRES_DB`

Vous pouvez ainsi visualiser, modifier et administrer vos tables et données facilement.
