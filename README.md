# hackathon-idfm

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
