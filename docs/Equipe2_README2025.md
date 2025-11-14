# [Projet REG'INNA]

## Présentation du projet

Ce projet a été développé dans le cadre du Hackathon Mobilités 2025, organisé par Île-de-France Mobilités les 13 et 14 novembre 2025. Pour en savoir plus, voici le [Guide des participants et participantes](https://github.com/hackathons-mobilites/hackathon_mobilites_2025/).

Ce projet répond au **Défi 4 - Accessibilité et confort des usagers des transports publics**

### Le problème et la proposition de valeur 

En fauteuil roulant depuis l’adolescence, Ilseem Jung, n’habite qu’à quelques minutes de Denfert-Rochereau et la ligne 6 du métro à Paris (XIVe). Pourtant, voilà plus d’un an qu’elle n’y a pas mis les pieds.
« Je ne m’y risque plus, certaines ne sont pas du tout adaptées. 
Je peux rentrer à Denfert, mais je ne peux pas sortir de beaucoup d’autres stations », témoigne la correspondante Île-de-France pour l’Association nationale pour la prise en compte du handicap dans les politiques publiques et privées (APHPP).

Rendre accessible le réseau de transport en île de France est un vrai défi et va durer plusieurs années. La priorisation des actions est essentielle pour les personnes en charge de la maintenance des équipements et des de celles en charge des programmes de mécanisation ou de rénovation des stations et des gares ainsi que pour le du programme "Métro pour tous".

**Nos usagers cibles** sont  : 
- les décideurs des projets de rénovation, de mécanisation et de mise en accessibilité du réseau 
- les mainteneurs sur le réseau

### La solution
Il s'agit d'un démonstrateur agrégeant sur une même carte  : 
* la facilité d'accès des gares et stations, 
* les lieux générateurs de flux PMR (établissements spécialisés pour enfance/jeunesse handicapée, établissements et services pour adultes handicapé, établissements hospitaliers, Gares) 
* les stations et gares sur lesquelles les validations de personnes âgées sont les plus importantes (validations de forfaits améthyste)
* des indicateurs d'accessibilité de la station calculés à partir des descriptions textuelles du site métro-connexion

Et calculant (et affichant sur la carte) un indicateur de type **score d'accessibilité** de chaque station et gare du réseau afin d'aider les mainteneurs et les décideurs à prioriser les chantiers de rénovation et de mise en accessibilité du réseau.

## Les données mobilisées :

### Données des niveaux d'accessibilité des stations extraites du [Plan PMR](https://eu.ftp.opendatasoft.com/stif/PlansRegion/Plans/Paris_PMR.pdf)

Par station et par ligne nous avons récupéré le niveau d'accessibilité issu de la carte PMR : 
1) Pastille Verte entourée de noir: **Très facile d'accès** (ascenseur ou plain-pied)
2) Pastille Noire entourée de vert : **Facile d'accès**, équipée d'escalator ou ascenseur sur tout le parcours entre la rue et le quai
3) Pastille Jaune : **Équipée d'au moins un escalator ou ascenseur** sur le parcours entre la rue et le quai
4) Pastille blanche : **Comportant uniquement des escaliers et peu profonde** (dénivelé de moins de 10m, le plus souvent entre 6 et 8 mètres (équivalent à 2 étages))
5) Pastille grise : **Comportant uniquement des escaliers et profonde** (dénivelé de plus de 10m)

### Données open sources utilisées

1) [Référentiel IDFM des stations du réseau] (https://data.iledefrance-mobilites.fr/explore/dataset/arrets-lignes/information/?disjunctive.route_long_name&disjunctive.id) (périmètre géographique issu du plan PMR).

2) Jointure avec les noms de stations pour croiser avec les données de Metro Connexion.

3) Metro Connexion  : données de description des trajets de correspondance entre les lignes au sein d'une station mises à disposition gracieusement par IDFM pour ce Hackathon

4) Données de validation : nombre de validations par jour sur l'ensemble des abonnements (améthyste, imagine'R, Navigo, ...) => historique sur 9 mois : 
* [Données de validation T1](https://data.iledefrance-mobilites.fr/explore/dataset/validations-reseau-ferre-nombre-validations-par-jour-1er-trimestre/export/)
* [Données de validation T4](https://data.iledefrance-mobilites.fr/explore/dataset/validations-reseau-ferre-nombre-validations-par-jour-4eme-trimestre/export/)
* [Données de validation T3](https://data.iledefrance-mobilites.fr/explore/dataset/validations-reseau-ferre-nombre-validations-par-jour-3eme-trimestre/export/)
* [Données de validation T2](https://data.iledefrance-mobilites.fr/explore/dataset/validations-reseau-ferre-nombre-validations-par-jour-2eme-trimestre/export/)

5) Lieux générateurs de flux PMR (données 2013 avec établissements en construction ou prévus au delà):
- [Etablissements hospitaliers franciliens] (https://data.iledefrance.fr/explore/dataset/les_etablissements_hospitaliers_franciliens/information/)
- [Etablissements d'accueil d'adultes en situation de handicap] (https://data.iledefrance.fr/explore/dataset/etablissements_et_services_pour_adultes_handicapes/information/)
- [Etablissements d'accueil d'enfants en situation de handicap] (https://data.iledefrance.fr/explore/dataset/etablissements_et_services_pour_l_enfance_et_la_jeunesse_handicapee/information/)

Coordonnées géographiques de ces lieux pour les associer aux stations les plus proches.

6) Référentiel des ascenseurs IDFM (13/11/25 20h): [Etat des ascenseurs](https://prim.iledefrance-mobilites.fr/fr/jeux-de-donnees/etat-des-ascenseurs)

    Nombre d'ascenseurs par station

### Données consolidées : 
1) % de validations améthyste par station,
2) Facilité d'accès à une station (carte PMR),
3) Nombre d'ascenseurs par station,
4) Nombre d'établissements PMR proches par station (moins de 250m),
5) Nombre moyen de marches par station (ascendantes + descendantes), 
6) Nombre moyen de mètres à parcourir,  
7) Nombre d'étapes pour effectuer la correspondance (complexité)

==> Toutes ces données par station / par ligne et géolocalisées (latitude /longitude).

### Calcul du score d'accessibilité : 
1) Prise en compte de ces 7 dimensions d'analyse 
2) Classification par rapprochement de typologie de station (de A à E) :
_On s'est basé sur un algorithme simple, inspiré de la méthode des k-moyennes. On a décrété 5 profils-types de stations, sur lesquels des actions d'accessibilité sont plus ou moins prioritaires (1er profil : actions très prioritaires, 5e profil : actions peu prioritaires). On calcule ensuite la proximité de nos stations réelles avec ces 5 profils-types. Chaque station est enfin attribuée à la catégorie de son profil-type le plus proche._

### Les problèmes surmontés et les enjeux en matière de données
1) Difficulté d'exploitation des données de la carte PMR : 
    * Première passe LLM
    * Deuxième passe à la main
    * Facilité d'accès peut être différente selon la ligne empruntée d'une station

2) Extraire les données d'accessibilité d'une correspondance depuis la description textuelle de métro connexion

3) Jointure entre les données des différentes sources au niveau de l'identifiant station (pas d'identifiant unique). Stations orthographiées différemment. Reprise à la main

4) Difficile de trouver les données des établissements privés générateurs de flux PMR (EHPAD, hôpitaux, établissements d'accueil de personnes en situation de handicap, ...)

### Et la suite ? 

Le démonstrateur pourrait être enrichi avec d'autres sources de données génératrices de flux PMR (EHPAD, Cimetière...) et un état en temps réel des ascenseur (provenant de la GMAO RATP).

La carte pourrait être complétée par des filtres affichant différentes vues des stations et gares :
- selon leur niveau d'accessibilité (nomenclature IDFM)
- selon leur typologie d'adéquation offre/demande d'accessibilité
- vue maintenance pour prioriser les réparations sur les équipements (escaliers mécaniques et ascenseurs)

Un moteur de recommandations d'actions automatiques pourrait être ajouté et proposer une priorisation des actions par station ou gare : réparation, ajout d'ascenseur, ajout d'escalier mécanique.

Dans un second temps, en pouvant coupler cet outil à une recherche d'itinéraire, nos usagers cibles pourraient aussi être des personnes en situation de handicap (mental, moteur, visuel, auditif, dû à l'âge) pour leur permettre de trouver des **itinéraires réellement accessibles** (avec des équipements fonctionnels à l'instant t et le parcours dans la station extrait de Metro connexion).


## Installation et utilisation

### Installation :

Récupérer le code source (branche Equipe-2) : 
`git clone https://github.com/hackathons-mobilites/hackathon_mobilites_2025.git`

Installer les librairies python utilisées

```python
pip install -r requirements.txt
```

### Utilisation

1. **Lancements des notebooks** 
Lancement des deux notebooks présents dans le dossier Notebooks_process pour créer les tables :
  - `data/interim/metro_connexion_nombre_etape.parquet`  
  - `data/metro_conexion_qualif.parquet`
2. **Lancements du DataPrep** 
Executer le fichier python présent dans resultats/repository/dataprep/main.py

3. **Utilisation de la carte interactive**
```python
streamlit run resultats/repository/geoparquet_app/main.py
```


## Documentation Technique du framework

### Structure des données

Le projet utilise plusieurs sources de données brutes et intermédiaires :

- **Données brutes CSV** :  
  - Carte PMR : `data/raw/carte_pmr.csv`  
  - Référentiel des gares IDF : `data/raw/emplacement-des-gares-idf.csv`  
  - État des ascenseurs : `data/raw/etat-des-ascenseurs.csv`  
  - Établissements pour enfants/adultes handicapés et hôpitaux  
  - Validations du réseau ferré par trimestre

- **Données intermédiaires Parquet / GeoParquet** :  
  - `data/interim/carte_pmr.parquet`  
  - `data/interim/ref_gares.gpq`  
  - `data/interim/validation_pourcentage.parquet`  
  - `data/interim/etablissements.gpq`  
  - `data/interim/metro_connexion_nombre_etape.parquet`  
  - `data/metro_conexion_qualif.parquet`

- **Données finales** :  
  - Enrichies : `data/enrich/final_table.gpq`  
  - Avec classification : `data/enrich/final_table_with_class.gpq`


### Notebooks de préparation des données (dossier notebook_process)

Deux notebooks traitent les données de `data/raw/metro_connexion_corresp_idfm_ref.csv` :

1. **metro_connexion_llm.ipynb**  
   - **Objectif** : Calculer le nombre de mètres et d’escaliers montés grâce à un modèle LLM.  
   - **Sortie** : `data/interim/metro_connexion_nombre_etape.parquet` 

2. **metro_connexion_nombre_etape.ipynb**  
   - **Objectif** : Agréger les données pour obtenir le nombre total d’étapes pour chaque station.  
   - **Sortie** : `data/interim/metro_connexion_nombre_etape.parquet`  

Ces notebooks servent de pré-traitement pour le pipeline principal.

### Framework de transformation des données (dossier DataPrep)
#### Pipeline de traitement 

La pipeline se compose de plusieurs jobs orchestrés dans l’ordre suivant :

1. **Carte PMR** : extraction et nettoyage des données PMR.
2. **Établissements** : consolidation et nettoyage des établissements critiques.
3. **Référentiel gares IDF** : nettoyage et géocodage des stations.
4. **Validations réseau** : calcul des totaux et pourcentages par station.
5. **Enrichissement** : jointure de toutes les sources et calculs supplémentaires (LGF, ascenseurs, correspondances).
6. **Classification** : attribution des stations à des classes selon des métriques clés.


#### Description des Jobs

##### CartePmrJob
- **Objectif** : Nettoyer et transformer les données de la carte PMR.
- **Entrée** : `data/raw/carte_pmr.csv`
- **Sortie** : `data/interim/carte_pmr.parquet`
- **Principales étapes** :
  - Lecture CSV
  - Nettoyage du nom des stations
  - Création d’une colonne d’ordre (`facilite_acces_order`) à partir des codes couleur
  - Export au format Parquet

##### EtablissementJob
- **Objectif** : Consolider et normaliser les données d’établissements (adultes/enfants handicapés, hôpitaux)
- **Entrées** : CSVs d’établissements multiples
- **Sortie** : `data/interim/etablissements.gpq`
- **Principales étapes** :
  - Harmonisation des colonnes (lat, lng, raison sociale)
  - Suppression des coordonnées manquantes
  - Ajout du type d’établissement
  - Fusion des sources
  - Conversion en GeoDataFrame

##### RefGareIdfJob
- **Objectif** : Nettoyer et transformer le référentiel des gares IDF
- **Entrée** : `data/raw/emplacement-des-gares-idf.csv`
- **Sortie** : `data/interim/ref_gares.gpq`
- **Principales étapes** :
  - Lecture CSV
  - Nettoyage des noms de stations
  - Extraction des coordonnées depuis `geo_point_2d`
  - Conversion en GeoDataFrame
  - Export en GeoParquet

##### ValidationJob
- **Objectif** : Consolider les validations par station et calculer le pourcentage de validations "Amethyste"
- **Entrées** : Plusieurs fichiers Parquet trimestriels
- **Sortie** : `data/interim/validation_pourcentage.parquet`
- **Principales étapes** :
  - Lecture et concaténation des fichiers
  - Nettoyage des colonnes numériques
  - Calcul du total par station
  - Calcul du total "Amethyste" et pourcentage
  - Export au format Parquet

##### EnrichJob
- **Objectif** : Combiner toutes les sources de données et enrichir les stations avec des métriques supplémentaires
- **Entrées** :
  - `ref_gares.gpq`, `carte_pmr.parquet`, `validation_pourcentage.parquet`, `etablissements.gpq`, `etat-des-ascenseurs.csv`, correspondances métro
- **Sortie** : `data/enrich/final_table.gpq`
- **Principales étapes** :
  - Jointures des correspondances et métriques
  - Filtrage des stations PMR
  - Calcul des distances Haversine pour établissements critiques (LGF_250m / LGF_500m)
  - Comptage des ascenseurs par station
  - Export GeoParquet

##### ClassificationStationsJob
- **Objectif** : Classer les stations selon plusieurs critères (accessibilité, LGF, ascenseurs, escaliers, étapes)
- **Entrée** : `data/enrich/final_table.gpq`
- **Sortie** : `data/enrich/final_table_with_class.gpq`
- **Principales étapes** :
  - Sélection des colonnes pertinentes pour la classification
  - Définition des centres idéaux pour chaque classe
  - Attribution des stations à la classe la plus proche (inspiré de K-Means)
  - Mise à jour du GeoDataFrame
  - Export GeoParquet


### Utilisation de l'IA / Frugalité
Nous avons ponctuellement utilisé l'IA pour : 
* Extraire les données de complexité d'une correspondance à partir de la description textuelle de Metro Connexion
* Extraire les données de facilité d'accès de la carte PMR

## La licence

Le code et la documentation de ce projet sont sous licence [MIT](LICENSE).
