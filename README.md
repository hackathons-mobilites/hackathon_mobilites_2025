# Predict'Mob — Plateforme de Mobilité Éco-Responsable pour l'Île-de-France

**Predict'Mob** est une solution intelligente qui combine **anticipation des perturbations**, **alternatives éco-responsables** et **gamification RSE** pour accompagner les entreprises et leurs salariés vers une mobilité durable.

> 💡 **En bref** : Une plateforme qui anticipe les aléas de transport, propose des alternatives bas-carbone avec score RSE, et engage les salariés via la gamification tout en fournissant des indicateurs RSE aux entreprises.

---

## Présentation du projet

Ce projet a été développé dans le cadre du **Hackathon Mobilités 2025**, organisé par Île-de-France Mobilités les **13 & 14 novembre 2025**. Pour en savoir plus, voici le [Guide des participants et participantes](https://github.com/hackathons-mobilites/hackathon_mobilites_2025/).

---

## Le problème et la proposition de valeur

### 🚨 Les problèmes identifiés

Aujourd'hui, les Franciliens font face à plusieurs défis :

- **Subissent les aléas sans anticipation** : retards et suppressions de trains découverts au dernier moment
- **Manque d'alternatives pertinentes** : difficultés à trouver rapidement un plan B adapté (covoiturage, vélo, télétravail)
- **Pas de suivi de l'impact mobilité** : aucun outil simple pour mesurer l'empreinte carbone de ses déplacements
- **Entreprises sans indicateurs RSE** : manque de données fiables sur les trajets domicile-travail pour les Plans de Déplacements Entreprise (PDE)

### 🎯 Les usagers cibles

- **Salariés franciliens** effectuant des trajets domicile-travail quotidiens en train/RER
- **Entreprises** souhaitant améliorer leur bilan RSE et encourager les mobilités durables
- **Partenaires mobilité** (opérateurs de covoiturage, vélos en libre-service) souhaitant proposer des alternatives

### 💡 Notre proposition de valeur

**Predict'Mob** combine :
- ✅ **Alternatives éco-responsables avec score RSE** (covoiturage, vélo, télétravail) classées par impact environnemental
- ✅ **Anticipation intelligente** des perturbations et identification de hotspots (zones à risque)
- ✅ **Gamification** pour encourager les mobilités bas-carbone et l'adoption des alternatives
- ✅ **Reporting RSE** pour les entreprises avec indicateurs CO₂, trajets durables (consentement RGPD strict)
- ✅ **Écosystème ouvert** pour intégrer les partenaires mobilité (Karos, Véligo, Klaxit...)

---

## La solution

Predict'Mob repose sur **deux leviers complémentaires** orchestrés par un agent intelligent :

### 🌱 Levier A — Anticipation & Alternatives Éco-Responsables

**Objectif** : Anticiper les perturbations, identifier les zones à risque et proposer des alternatives bas-carbone avec score RSE.

**Fonctionnement** :
1. **Collecte & analyse** : Données PRIM, GTFS/GTFS-RT, Météo France + trajets habituels des employés
2. **Anticipation intelligente** : Algorithme ML identifiant les perturbations probables et les gares porteuses de risque
3. **Détection de hotspots** : Agrégation automatique des zones où plusieurs salariés sont impactés
4. **Génération d'alternatives** : Calcul automatique du **score RSE** (CO₂, temps, coût) pour chaque option de mobilité durable

**APIs principales** :
- `GET /v1/hotspots` : Zones à risque détectées en temps réel
- `GET /v1/alternatives` : Alternatives éco-responsables **classées par score RSE** (covoiturage, vélo, télétravail, bus de substitution)

### 🎮 Levier B — Mobility Tracker (Gamification + RSE)

**Objectif** : Engager les salariés dans une mobilité durable et fournir des indicateurs RSE aux entreprises.

#### Pour les salariés (Application mobile web)

- 📍 Déclarer ses déplacements (train, vélo, covoiturage, télétravail)
- 🏆 Gagner des points et badges selon les modes de transport durables
- ⚠️ Recevoir des alertes hotspots sur ses trajets habituels
- 🚴 Consulter des alternatives éco-responsables classées par score RSE (CO₂ évité, durée, coût)
- 🔒 Contrôler le partage de données avec l'entreprise (opt-in RGPD)

#### Pour les entreprises (Back-office Streamlit)

Tableau de bord RSE avec indicateurs agrégés (uniquement pour les salariés ayant activé le partage) :
- CO₂ évité, taux de mobilités durables, adoption des alternatives
- Graphiques et tendances
- Leaderboards par équipe
- Export PDE/RSE

---

## Données mobilisées

### Sources externes
- **PRIM** (Île-de-France Mobilités) : ponctualité et qualité de service des lignes train/RER
- **GTFS / GTFS-RT** : horaires théoriques et temps réel des transports franciliens
- **Météo France** : conditions météorologiques (facteur explicatif des retards)
- **SIRENE** (INSEE) : identification des entreprises via SIREN

### Données internes
Base PostgreSQL avec tables : `companies`, `employees`, `trajectories`, `predictions`, `hotspots`, `alternatives` (avec score RSE par option), `commute_logs`, `mobility_events`, `employee_points`, `company_rse_snapshot`.

### Respect de la vie privée
- ✅ Consentement explicite (opt-in) pour le partage avec l'entreprise
- ✅ RGPD compliant (droits d'accès, rectification, suppression)
- ✅ Anonymisation des agrégats RSE
- ✅ Transparence totale sur les données partagées

---

## Enjeux techniques & défis relevés

### 1. Fusion de sources hétérogènes (PRIM + GTFS + Météo)
**Défi** : Formats, fréquences et granularités différentes  
**Solution** : Pipeline ETL unifié, jointures temporelles et spatiales, gestion des données manquantes

### 2. Conversion trajet → gare porteuse du risque
**Défi** : Identifier quelle gare pose problème dans un trajet avec plusieurs correspondances  
**Solution** : Analyse historique des retards par gare, algorithme d'attribution du risque, pondération des correspondances critiques

### 3. Agrégation en hotspots
**Défi** : Grouper efficacement les trajets impactés pour maximiser l'utilité des alternatives  
**Solution** : Clustering spatial et temporel, seuil minimum de salariés impactés, priorisation selon l'urgence

### 4. Consentement strict RGPD
**Défi** : Permettre la gamification individuelle tout en respectant le choix de ne pas partager avec l'entreprise  
**Solution** : Table `employee_settings` avec champ `share_with_company`, filtrage systématique des requêtes RSE, interface claire

### 5. Gamification compatible entreprises
**Défi** : Motiver individuellement sans créer de pression ou compétition toxique  
**Solution** : Points personnels visibles uniquement par le salarié (sauf opt-in), leaderboards anonymisés par équipes, badges célébrant la diversité des efforts

### 6. Écosystème ouvert pour partenaires
**Défi** : Intégrer des opérateurs de mobilité (Karos, Klaxit, Véligo…) sans refonte complète  
**Solution** : Endpoint `/partner/alternatives` pour propositions tierces, format standardisé avec calcul automatique du score RSE (CO₂ évité, durée, coût) pour classer les alternatives selon leur impact environnemental

---

## Recommandations pour Île-de-France Mobilités

### 1. APIs temps réel plus accessibles
**Observation** : Les données GTFS-RT sont fragmentées selon les opérateurs  
**Recommandation** : API unifiée pour tous les modes avec latence < 30s et documentation claire des cas d'usage

### 2. Historique de ponctualité enrichi
**Observation** : Les données PRIM pourraient être plus granulaires  
**Recommandation** : Historique par gare et tranche horaire, raisons de retard catégorisées, format optimisé pour le ML

### 3. Référentiel des alternatives de mobilité
**Observation** : Difficile de connaître toutes les options disponibles selon la zone  
**Recommandation** : Référentiel ouvert des services de mobilité partagée, API géolocalisée, partenariats formalisés

### 4. Sandbox pour tester avant production
**Observation** : Le passage du hackathon à la production nécessite des tests approfondis  
**Recommandation** : Environnement de test avec données anonymisées, rate limits adaptés au développement, documentation "Getting Started"

---

## Et la suite ?

### 🤖 Vision : Agent Intelligent de Mobilité Éco-Responsable

Notre roadmap converge vers un **agent autonome** orchestrant l'ensemble des moteurs (prédiction, hotspots, alternatives) avec un **calcul RSE en temps réel** :

```
┌─────────────────────────────────────────────────────┐
│     AGENT MOBILITÉ ÉCO-RESPONSABLE (AME)           │
│                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │  Predict    │→ │   Hotspot    │→ │  Score    │ │
│  │  Engine     │  │   Engine     │  │  RSE      │ │
│  └─────────────┘  └──────────────┘  └───────────┘ │
│         ↓                ↓                 ↓        │
│  ┌──────────────────────────────────────────────┐  │
│  │    Moteur d'Optimisation Multi-Objectifs    │  │
│  │  (temps, coût, CO₂, confort, préférences)   │  │
│  └──────────────────────────────────────────────┘  │
│         ↓                                           │
│  ┌──────────────────────────────────────────────┐  │
│  │   Recommandations Personnalisées + Impact   │  │
│  │        RSE (individuel & entreprise)         │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**Fonctionnement** : L'agent analyse en continu les données de mobilité, anticipe les perturbations, calcule automatiquement le score RSE de chaque alternative (CO₂, temps, coût) et propose la meilleure option selon le contexte et les préférences de l'utilisateur, tout en alimentant les indicateurs RSE de l'entreprise.

### 🚀 Court terme (1-3 mois)
- **Intégration partenaires mobilité** : Karos, Klaxit (covoiturage), Véligo, Lime (vélos) avec scoring RSE automatique
- **Prédiction multi-modes** : Étendre aux bus, métro, tram (pas seulement train/RER)
- **Notifications push proactives** : Alertes + alternatives éco-responsables dès 7h le matin

### 🌟 Moyen terme (3-6 mois)
- **Agent d'optimisation multi-critères** : IA combinant prédiction, alternatives et calcul RSE en temps réel
- **Apprentissage des préférences** : L'agent apprend des choix passés pour affiner les recommandations
- **PDE complet** : Simulation d'impact, générateur automatique, intégration outils RH avec métriques RSE automatisées

### 🔭 Long terme (6-12 mois)
- **Agent autonome décisionnel** : L'AME devient un copilote mobilité personnel avec scoring RSE prédictif
- **API publique & Marketplace** : Ouvrir l'écosystème aux développeurs et partenaires mobilité
- **Impact social** : Quartiers mal desservis, accessibilité PMR, partenariats associatifs avec calcul d'impact RSE global

---

## Architecture technique

### Stack retenu
- **Backend API** : FastAPI (Python 3.11)
- **Base de données** : PostgreSQL 15 (schéma fourni par l'équipe Data avec image Docker)
- **Module IA** : scikit-learn + XGBoost (fourni par l'équipe Data)
- **Back-office Entreprise** : Streamlit
- **App Mobile Salarié** : HTML/CSS/JS (web mobile responsive)
- **Orchestration** : Docker Compose

### Flux de données
1. APIs PRIM, GTFS, Météo → Module Predict → Table `predictions`
2. Engine hotspots → Table `hotspots`
3. API Backend → App Mobile (alertes + alternatives)
4. Salarié déclare trajet → Tables `commute_logs` + `mobility_events`
5. Calcul points/badges → Table `employee_points`
6. Agrégation RSE (si opt-in) → Table `company_rse_snapshot` → Back-office

---

## Équipe

| Rôle | Prénom | Responsabilités |
|------|--------|-----------------|
| **Architecture & Product** | Sofiene | Architecture technique, coordination, David : product vision |
| **Data Science** | Marc + Marc Stephane : Data | Module IA de prédiction, pipeline ML, base de données |
| **Backend** | Gabriel | API FastAPI, logique métier, intégration BDD |base de données
| **Frontend** | Sami | Back-office Streamlit, visualisations, dashboards |
| **UX/UI Design** | David & Sami & Sofiene | Maquettes, wireframes, app mobile web |

---

## La licence

Le code et la documentation de ce projet sont sous licence **MIT**.

Voir le fichier [LICENSE](LICENSE) pour le texte complet.

---

**🏆 #HackathonMobilites2025 #PredictMob #MobilitéDurable #OpenData #IDFM**
