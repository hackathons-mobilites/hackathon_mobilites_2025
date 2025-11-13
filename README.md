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

- Access the application
Open your web browser and navigate to `http://localhost:8501` to access the application.
