# [Projet REG'INNA]

## Présentation du projet

Ce projet a été développé dans le cadre du Hackathon Mobilités 2025, organisé par Île-de-France Mobilités les 13 et 14 novembre 2025. Pour en savoir plus, voici le [Guide des participants et participantes](https://github.com/hackathons-mobilites/hackathon_mobilites_2025/).

Ce projet répond au Défi 4 - Accessibilité et confort des usagers des transports publics 

### Le problème et la proposition de valeur 

En fauteuil roulant depuis l’adolescence, Ilseem Jung, n’habite qu’à quelques minutes de Denfert-Rochereau et la ligne 6 du métro à Paris (XIVe). Pourtant, voilà plus d’un an qu’elle n’y a pas mis les pieds.
« Je ne m’y risque plus, certaines ne sont pas du tout adaptées. 
Je peux rentrer à Denfert, mais je ne peux pas sortir de beaucoup d’autres stations », témoigne la correspondante Île-de-France pour l’Association nationale pour la prise en compte du handicap dans les politiques publiques et privées (APHPP).

Rendre accessible le réseau de transport en île de France est un vrai défi et va durer plusieurs années. La priorisation des actions est essentielle pour les personnes en charge de la maintenance des équipements et des de celles en charge des programmes de mécanisation ou de rénovation des stations et des gares ainsi que pour le du programme "Métro pour tous".

**Nos usagers cibles** sont  : 
- les mainteneurs sur le réseau
- les décideurs des projets de rénovation, de mécanisation et de mise en accessibilité du réseau 

### La solution
Il s'agit d'un démonstrateur agrégeant sur une même carte  : 
* la facilité d'accès des gares et stations, 
* les lieux générateurs de flux PMR (établissements spécialisés pour enfance/jeunesse handicapée, établissements et services pour adultes handicapé, établissements hospitaliers, Gares) 
* les stations et gares sur lesquelles les validations de personnes âgées sont les plus importantes (validations de forfaits améthyste)
* l'état des ascenseurs et escaliers mécaniques des espaces.

Et calculant (et affichant sur la carte) un indicateur de type **score d'accessibilité** chaque station et gare du réseau afin d'aider les mainteneurs et les décideurs à prioriser les chantiers de rénovation et de mise en accessibilité du réseau.

## Les données mobilisées :

### Données des niveaux d'accessibilité des stations extraites du [Plan PMR](https://eu.ftp.opendatasoft.com/stif/PlansRegion/Plans/Paris_PMR.pdf)

Par station et par ligne nous avons récupéré le niveau d'accessibilité issu de la carte PMR : 
1) Pastille Verte entourée de noir: **Très facile d'accès** (ascenseur ou plain-pied)
2) Pastille Noire entourée de vert : **Facile d'accès**, équipée d'escalator ou ascenseur sur tout le parcours entre la rue et le quai
3) Pastille Jaune : **Équipée d'au moins un escalator ou ascenseur** sur le parcours entre la rue et le quai
4) Pastille blanche : **Comportant uniquement des escaliers et peu profonde** (dénivelé de moins de 10m, le plus souvent entre 6 et 8 mètres (équivalent à 2 étages))
5) Pastille grise : **Comportant uniquement des escaliers et profonde** (dénivelé de plus de 10m)

### Données open sources utilisées

1) Référentiel IDFM des stations du réseau (périmètre géographique issu du plan PMR).

2) Jointure avec les noms de stations pour croiser avec les données de Metro Connexion.

3) Metro Connexion  : données de description des trajets de correspondance entre les lignes au sein d'une station.

4) Données de validation : nombre de validations par jour sur l'ensemble des abonnements (améthyste, imagine'R, Navigo, ...) => historique sur 9mois

5) Lieux générateurs de flux PMR (données 2013 avec établissements en construction ou prévus au delà):
            - Etablissements hospitaliers franciliens 
            - Etablissements d'accueil d'adultes en situation de handicap
            - Etablissements d'accueil d'enfants en situation de handicap
    Coordonnées géographiques de ces lieux pour les associer aux stations les plus proches

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

==> toutes ces données par station/ par ligne et géolocalisée (latitude /longitude) 

### Calcul du score d'accessibilité : 
1) Prise en compte des 7 dimensions d'analyse 
2) Classification par rapprochement de typologie de station (de A à E)

### Les problèmes surmontés et les enjeux en matière de données
1) Difficulté d'exploitation des données de la carte PMR : 
    - Première passe LLM
    - Deuxième passe à la main
    - Facilité d'accès peut être différente selon la ligne empruntée d'une station

2) Extraire les données d'accessibilité d'une correspondance depuis la description textuelle de métro connexion

3) Jointure entre les données des différentes sources au niveau de l'identifiant station (pas d'identifiant unique). Stations orthographiées différemment. Reprise à la main

4) Difficile de trouver les données des établissements privés générateurs de flux PMR (EHPAD, hôpitaux, établissements d'accueil de personnes en situation de handicap, ...)

### Et la suite ? 
> [!TIP]
> Ici vous vous projetez sur comment vous auriez aimé développer votre projet si vous aviez eu plus de temps ! (Quel cas d'usage pour la suite ? Quelles ressources à mobiliser ?)

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

Créer le jeu de données, lancer:

**Note**: Les données de qualification de la carte sont sur `data/enrich/final_table_with_class.gbq`, la commande n'est pas nécessaire, seulement pour 
reconstuire la source.

```python
python resultats/repository/dataprep/main.py
```


### Fonctionnement

**Utilisation de la carte interactive**

```python
streamlit run resultats/repository/geoparquet_app/main.py
```


### Utilisation de l'IA / Frugalité
Nous avons ponctuellement utilisé l'IA pour : 

- Extraire les données de complexité d'une correspondance à partir de la description textuelle de Metro Connexion

- Extraire les données de facilité d'accès de la carte PMR

## La licence

Le code et la documentation de ce projet sont sous licence [MIT](LICENSE).
