# Interface d'Accessibilité PMR pour les Transports en Commun

Ce projet a été développé dans le cadre du Hackathon Mobilités 2025, organisé par Île-de-France Mobilités les 13 et 14 novembre 2025. Pour en savoir plus, voici le [Guide des participants et participantes](https://github.com/hackathons-mobilites/hackathon_mobilites_2025/).

Une interface web complète qui permet aux personnes à mobilité réduite (PMR) d'analyser l'accessibilité de leurs trajets en transports en commun avec des informations détaillées, des scores quantifiés et des guides pratiques étape par étape.

## Présentation du projet

### Le problème et la proposition de valeur 

**Le problème :** Les personnes à mobilité réduite font face à de nombreux défis lors de leurs déplacements en transports en commun :
- Manque d'informations fiables sur l'accessibilité des gares et véhicules
- Absence de guidance détaillée pour les correspondances complexes
- Difficultés à planifier des trajets en fonction de leurs besoins spécifiques
- Informations dispersées et peu exploitables pour une prise de décision éclairée

**Les usagers cibles :**
- Personnes en fauteuil roulant
- Personnes avec des déficiences visuelles ou auditives
- Personnes avec des difficultés de mobilité temporaires ou permanentes
- Accompagnants et aidants
- Professionnels du secteur médico-social

### La solution

**Notre solution :** Une interface web complète qui combine multiple sources de données pour offrir :

🔍 **Analyse automatique d'accessibilité** avec calcul de scores quantifiés (0-100%) pour :
- Accessibilité visuelle (annonces visuelles)
- Accessibilité sonore (annonces audio)
- Accessibilité PMR globale (gares + véhicules + équipements)

🧭 **Guides détaillés étape par étape** incluant :
- Instructions précises pour les correspondances ("En tête, un couloir perpendiculaire...")
- Recommandations de positionnement dans les rames
- Guides de sortie détaillés pour les stations de destination

📊 **Données mobilisées :**
- API Navitia pour les itinéraires et informations de transport
- `accessibilite-en-gare.csv` - Niveaux d'accessibilité des gares
- `positionnement-dans-la-rame.csv` - Recommandations de positionnement
- `metro_connexion_corresp_idfm_ref.csv` - Descriptions détaillées des correspondances
- `metro_connexion_sorties_idfm_ref.csv` - Instructions de sortie des stations

**Fonctionnement :**
1. L'utilisateur colle une URL de requête Navitia (avec départ/arrivée/horaires)
- Nous avons utilisé la requête ```https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/journeys?from=stop_area%3AIDFM%3A71056&to=stop_area%3AIDFM%3A72132&datetime=20251113T142800&```,, qui simule un trajet de Denfert-Rochereau à Asnières le 13 novembre 2025 à partir de 14h28.
2. Le système interroge l'API Navitia et enrichit les données avec les CSV
3. Calcul automatique des scores d'accessibilité par section
4. Affichage d'un itinéraire détaillé avec guides pratiques et recommandations

### Les problèmes surmontés et les enjeux en matière de données

**Problèmes techniques surmontés :**
- **Hétérogénéité des formats de données** → Développement de parseurs robustes pour différents formats CSV et API
- **Correspondance entre identifiants** → Implémentation de fonctions de nettoyage et d'extraction d'IDs
- **Calcul de scores cohérents** → Création d'algorithmes de scoring prenant en compte multiple critères
- **Interface utilisateur complexe** → Design d'une interface claire malgré la richesse des informations

**Recommandations à Île-de-France Mobilités :**

🔧 **Standardisation des données :**
- Uniformiser les identifiants de stations entre différentes sources
- Standardiser les formats de données d'accessibilité
- Fournir une API unifiée pour l'accessibilité

📍 **Enrichissement des données :**
- Données temps réel sur l'état des équipements (ascenseurs, escalators)
- Informations sur la largeur des couloirs et espaces d'attente
- Données de géolocalisation précise des équipements dans les stations

🔄 **Amélioration de l'API Navitia :**
- Inclusion native des scores d'accessibilité dans les réponses
- Informations détaillées sur les équipements de transfert
- Support des requêtes d'accessibilité spécialisées

### Et la suite ?

**Développements futurs envisagés :**

🎯 **Fonctionnalités avancées :**
- **Interface de saisie intuitive** → Recherche départ/arrivée directe sans URL complexe
- **Mode navigation GPS** → Guidage vocal étape par étape pendant le trajet
- **Signalement collaboratif** → Permettre aux usagers de signaler des problèmes d'accessibilité
- **Profils utilisateur personnalisés** → Adaptation aux besoins spécifiques (type de handicap, équipements)
- **Intégration temps réel** → État des ascenseurs et équipements en direct

📱 **Applications mobiles :**
- Application iOS/Android native avec notifications push
- Mode hors-ligne pour les trajets fréquents
- Intégration avec les assistants vocaux

🌐 **Extension géographique :**
- Déploiement sur d'autres régions françaises
- Adaptation aux données des autres autorités organisatrices
- Support international avec adaptation aux standards locaux

**Ressources nécessaires :**
- Partenariats avec les associations de personnes handicapées
- Accès aux APIs temps réel des équipements
- Financement pour le développement mobile et les tests utilisateurs

## Installation et utilisation

### Prérequis
- Navigateur web moderne (Chrome, Firefox, Safari, Edge)
- Connexion internet pour l'API Navitia

### Installation
1. Cloner ou télécharger le projet
```bash
git clone [url-du-repo]
cd hackaton
```

2. Ouvrir `interface_complete.html` dans un navigateur web

### Utilisation

1. **Préparer une requête Navitia :**
   - Aller sur l'API Navitia ou utiliser un service de planification de trajet
   - Copier l'URL complète de la requête de trajet (ex: `https://api.navitia.io/v1/coverage/fr-idf/journeys?from=...&to=...`)
   - Coller cette URL dans le champ "URL de la requête Navitia"

2. **Charger les données (optionnel) :**
   - Uploader les fichiers CSV pour des données enrichies
   - Ou utiliser les données de démonstration intégrées

3. **Analyser l'accessibilité :**
   - Cliquer sur "🔍 Analyser l'accessibilité"
   - Consulter les scores et informations détaillées

4. **Naviguer dans les résultats :**
   - **Onglet Itinéraire** : Visualisation détaillée avec guides pratiques
   - **Onglet Légende** : Explication des scores et symboles
   - **Onglet JSON** : Données brutes pour développeurs

### Structure des fichiers
```
hackaton/
├── interface_complete.html      # Interface web principale
├── appel_api.py                # Script Python pour l'API Navitia
├── functions_score.py          # Fonctions de calcul des scores
├── accessibilite-en-gare.csv   # Données d'accessibilité (optionnel)
├── positionnement-dans-la-rame.csv  # Recommandations de positionnement (optionnel)
├── metro_connexion_corresp_idfm_ref.csv  # Guides de correspondances (optionnel)
├── metro_connexion_sorties_idfm_ref.csv  # Guides de sorties (optionnel)
└── README.md                   # Ce fichier
```

## La licence

Le code et la documentation de ce projet sont sous licence [MIT](LICENSE).

Cette licence permissive permet la réutilisation, modification et distribution du code, y compris dans des projets commerciaux, tout en préservant les crédits aux auteurs originaux.