# hackathon-idfm
 
# Présentation du projet
 
Ce projet a été développé dans le cadre du Hackathon Mobilités 2025, organisé par Île-de-France Mobilités les 13 et 14 novembre 2025.
 
L’objectif : offrir une expérience de déplacement en vélo fluide et multimodale pour les usagers urbains.
 
Cet outil aide les utilisateurs à planifier un itinéraire vélo en intégrant plusieurs options de mobilité. Il permet de :
- Rechercher un trajet sur la carte.
- Trouver des emplacements pour garer son vélo.
- Visualiser les correspondances avec d’autres modes de transport (métro, bus, etc.).
- Afficher le Chemin à pied entre les points d’intérêt et les connexions.
 
# Le problème et la proposition de valeur
 
Aujourd’hui, il n’existe pas d’outil qui priorise réellement le point de vue du cycliste. Les solutions actuelles ne permettent pas de planifier un itinéraire en tenant compte des parkings vélo les plus proches le long du trajet.
De plus, les cyclistes manquent de visibilité sur les connexions multimodales (RER, Tram) qui leur offriraient la possibilité de embarquer leur vélo pour optimiser leur déplacement.
 
Notre proposition de valeur : offrir une application qui place le cycliste au centre, en lui permettant de planifier son trajet complet, avec des options multimodales et des informations pratiques pour une mobilité fluide, flexible et durable.
 
# La solution
 
Nous avons développé une application open source qui permet à l’utilisateur de rechercher facilement un itinéraire et d’obtenir le meilleur trajet, en tenant compte du parking vélo le plus proche.
Elle propose également des fonctionnalités avancées :
 
Choix du mode de trajet : standard, sécurisé ou rapide.
Affichage des conditions météo.
Durée estimée du parcours.
Options multimodales : possibilité de combiner vélo avec métro, bus ou marche à pied, en prenant en compte les connexions où l’utilisateur peut embarquer son vélo.
 
Cette solution répond au besoin initial : faciliter la mobilité urbaine en offrant une expérience fluide, personnalisée et durable, tout en mettant en avant les connexions multimodales pour optimiser le trajet.
 
# Les problèmes surmontés et les enjeux en matière de données
 
L’un des principaux défis rencontrés a été la nécessité de combiner deux solutions distinctes pour répondre à notre objectif :
 
Calculateur d’itinéraires vélo – Geovelo
Calculateur Île-de-France Mobilités – Accès générique (v2)
 
Cette intégration était essentielle pour offrir une expérience complète, car aucune API unique ne permettait de gérer à la fois les itinéraires vélo et les connexions multimodales (RER, métro, bus), tout en prenant en compte la possibilité pour l’utilisateur d’embarquer son vélo.
 
# Et la suite ?
 
Pour aller plus loin, plusieurs évolutions sont envisagées afin d’améliorer l’expérience utilisateur :
 
Intégration en temps réel des données de trafic et des perturbations (métro, RER, routes).
Alertes personnalisées (météo défavorable, travaux, indisponibilité des parkings vélo).
Système de recommandations basé sur les préférences de l’utilisateur (trajet le plus vert, le plus rapide, le plus sécurisé).
Visualisation des émissions CO₂ évitées pour encourager la mobilité durable.
Mode hors ligne pour consulter les itinéraires sans connexion.
 
# Installation et utilisation
 
Installation steps:
 
- Clone the repository
- Install virtual environment
 
```bash
virtualenv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```
 
- Install dependencies
 
```bash
pip install -r requirements.txt
```
 
- Set up environment variables
Create a `.env` file in the root directory and add the necessary environment variables.
 
```bash
cp .env.example .env
```
 
- Run the application
 
```bash
python3 src/parking_velo/domain/apps/load_parking_velo_data.py
python3 src/parking_velo/domain/apps/create_filtered_parking_velo_data.py
streamlit run app.py
```
 
- Sidebar options
 
Dans la barre latérale (expander "⚙️ Options") vous pouvez :
 
- Cocher "Afficher les parkings vélo sur la carte" pour visualiser les emplacements.
- Cocher "Passer par un parking vélo proche de l'arrivée (segment marche)" :
    - Si coché (valeur par défaut) l'itinéraire vélo s'arrête au parking le plus proche puis un segment de marche est ajouté jusqu'à la destination finale (clé `itinerary_marche` présente dans la réponse).
    - Si décoché l'itinéraire vélo va directement jusqu'à la destination et la clé `itinerary_marche` est absente.
 
- Access the application
Open your web browser and navigate to `http://localhost:8501` to access the application.
 
# La licence
 
Le code et la documentation de ce projet sont sous licence MIT.
