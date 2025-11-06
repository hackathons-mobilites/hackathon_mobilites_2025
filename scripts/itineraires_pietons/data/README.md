# Données — itinéraires piétons

Ce dossier contient les fichiers d'entrée et la documentation minimale pour les GeoJSON générés représentant des itinéraires piétons (un fichier GeoJSON par itinéraire arrêt → POI).

## Fichiers sources attendus

- `POI_IDF.csv` — points d'intérêt. Colonnes attendues (minimum) : `id`, `nom_poi`, `type_lieu`, `poi_lat`, `poi_lon`.
- `referentiel_arret_derniere_version.parquet` — référentiel des arrêts. Colonnes attendues (minimum) : `ArRId`, `ArRName`, `ArRLatitude`, `ArRLongitude`, `ArRType`, `INSEE_COM`, `nom_epci`, `nom_commune_standard`, `nom_departement`.
- `poi_types_relevant.txt` — liste (une valeur par ligne) des `type_lieu` retenus pour générer des itinéraires (filtres métiers).

Placez ces fichiers dans ce dossier pour que le package (`itineraires_pietons`) puisse les charger via sa configuration.

## Méthode

- Filtrage des POI par `type_lieu` (cf. `poi_types_relevant.txt`).
- Recherche des POI proches de chaque arrêt (KDTree + calcul de distance de type haversine, rayon par défaut 500 m).
- Pour chaque paire arrêt → POI trouvée, calcul d'un itinéraire piéton via Valhalla (profil `pedestrian`) et export d'un GeoJSON indépendant contenant la géométrie et les propriétés.

Cette méthode produit un fichier GeoJSON par itinéraire afin de faciliter la sélection, la distribution et l'utilisation par défi.

## Convention de nommage des fichiers

Chaque GeoJSON généré suit le format de nommage suivant :

`{CODE_INSEE}_{NOM_ARRET}_{POI_UID_OR_ID}.geojson`

- `CODE_INSEE` : code INSEE de la commune de l'arrêt (ex. `75056`).
- `NOM_ARRET` : nom de l'arrêt (espaces remplacés par `_`, caractères problématiques nettoyés).
- `POI_UID_OR_ID` : identifiant unique du POI. Si le champ `id` d'origine est présent et unique il est utilisé, sinon le pipeline génère un `poi_uid` stable (index interne). Les `/` et caractères non valides sont remplacés par `_`.

Exemple de nom : `93055_Gare_Clichy_12345.geojson`

Le dossier de sortie par défaut est `itineraires_pietons/data/output/` (configurable dans le code).

## Contenu d'un GeoJSON (structure)

Chaque fichier est un `FeatureCollection` contenant une seule `Feature` avec :

- geometry : LineString (itinéraire Valhalla — liste de [lon, lat]).
- properties : dictionnaire avec au minimum les champs suivants :

	- `arret_id` : identifiant de l'arrêt (`ArRId`).
	- `arret_nom` : nom lisible de l'arrêt.
	- `arret_type` : type d'arrêt (rail / metro / tram).
	- `poi_id` : identifiant POI d'origine (ou `poi_uid` si généré).
	- `poi_nom` : nom du POI.
	- `poi_type` : valeur de `type_lieu` du POI.
	- `distance_vol_oiseau` : distance à vol d'oiseau (m), calculée entre arrêt et POI.
	- `distance_reelle` : distance estimée fournie par Valhalla (m) — lorsque disponible.
	- `duree_marche` : durée de marche estimée (minutes) — lorsque disponible.
	- `code_insee` : code INSEE de la commune de l'arrêt.
	- `commune` : nom de la commune (normalisé si présent).
	- `epci` : nom de l'EPCI si présent.
	- `departement` : nom du département si présent.

Ces champs permettent un tri, un croisement ou une agrégation simple pour chaque itinéraire.

## Cas d'usage — exemples pour les défis du hackathon

Ces GeoJSONs sont pensés pour être immédiatement utilisables par des scripts, des outils SIG ou des applications web légères.

- 🔧 Défi 1 — Mobilités actives et intermodalité : évaluation d'impact et propositions d'outils

	Utilisez les itinéraires pour mesurer les temps d'accès piéton aux POI stratégiques (emplois, services). Par exemple, calculez la part des arrêts desservant des POI accessibles en moins de 10 minutes à pied et proposez des améliorations (nouveaux arrêts, micro-mobilité, aménagements piétons).

- 🚌 Défi 2 — Outils à destination des entreprises

	Croisez les itinéraires avec des données d'implantation d'entreprises pour proposer des recommandations de localisation (accessibilité piétonne vers services / gares) et estimer l'attractivité d'un site pour les salariés (temps de trajet domicile→arrêt→POI).

- 🛑 Défi 3 — Outils à destination des collectivités territoriales

	Agrégez les GeoJSONs par EPCI / commune pour identifier les secteurs sous‑desservis à pied et prioriser des interventions (trottoirs, traversées piétonnes, signalisation). Produisez des cartes thématiques (zones < 5 min / 10 min) et un rapport de valeur socio‑spatiale.

- 🛋️ Défi 4 — Accessibilité et confort des usagers

	- Analysez les durées et distances réelles fournies par Valhalla pour détecter des itinéraires qui semblent longs par rapport à la distance à vol d'oiseau (zones qui pourraient gagner en accessibilité via améliorations d'infrastructures ou équipements pour l'accessibilité PMR).
	- Croiser les données d'itinéraires piétons avec les données de marchabilité à l'ombre ou l'indice canopée de SQY par exemple pour favoriser la plantation d'arbres à proximité des stations.
