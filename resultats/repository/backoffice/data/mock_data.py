import pandas as pd
from datetime import datetime, timedelta
import random

# Entreprises fictives
COMPANIES = [
    {"id": 1, "name": "Acme Corp", "siren": "123456789", "sector": "Tech"},
    {"id": 2, "name": "GreenTech SA", "siren": "987654321", "sector": "Environnement"},
]

# Sites d'entreprise
SITES = [
    {"id": 1, "company_id": 1, "name": "Siège Paris", "address": "10 rue de Rivoli, 75001 Paris"},
    {"id": 2, "company_id": 1, "name": "Bureau La Défense", "address": "1 Esplanade du Général de Gaulle, 92400 Courbevoie"},
    {"id": 3, "company_id": 2, "name": "Campus Saclay", "address": "Route de l'Orme aux Merisiers, 91190 Saint-Aubin"},
]

# Salariés fictifs
EMPLOYEES = []
for i in range(1, 51):
    company_id = 1 if i <= 30 else 2
    EMPLOYEES.append({
        "id": i,
        "company_id": company_id,
        "email": f"employe{i}@example.com",
        "home_postcode": random.choice(["75001", "92400", "91190", "77000", "94000"]),
        "opt_in": random.choice([True, True, True, False]),  # 75% opt-in
    })

# Hotspots fictifs
HOTSPOTS = [
    {
        "id": 1,
        "gare_name": "Gare de Lyon",
        "datetime_debut": datetime.now().replace(hour=8, minute=30),
        "nb_trajets_affectes": 12,
        "risk_level": "high",
    },
    {
        "id": 2,
        "gare_name": "Gare du Nord",
        "datetime_debut": datetime.now().replace(hour=9, minute=0),
        "nb_trajets_affectes": 8,
        "risk_level": "medium",
    },
    {
        "id": 3,
        "gare_name": "Saint-Lazare",
        "datetime_debut": datetime.now().replace(hour=7, minute=45),
        "nb_trajets_affectes": 5,
        "risk_level": "low",
    },
]

# Métriques RSE fictives
def get_rse_metrics(company_id, period="month"):
    employees_with_optin = [e for e in EMPLOYEES if e["company_id"] == company_id and e["opt_in"]]
    nb_participants = len(employees_with_optin)
    
    return {
        "co2_saved_kg": round(random.uniform(150, 350), 1),
        "nb_trajets_partages": random.randint(50, 120),
        "nb_trajets_durables": random.randint(30, 80),
        "covoiturage_rate": round(random.uniform(0.2, 0.4), 2),
        "nb_participants": nb_participants,
        "total_employees": len([e for e in EMPLOYEES if e["company_id"] == company_id]),
    }

# Évolution CO2 sur 30 jours
def get_co2_evolution(company_id):
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30, 0, -1)]
    values = [round(random.uniform(5, 15), 1) for _ in dates]
    return pd.DataFrame({"date": dates, "co2_saved_kg": values})

# Répartition des modes de transport
def get_mobility_distribution(company_id):
    return pd.DataFrame({
        "mode": ["Covoiturage", "Vélo", "Télétravail", "Transport en commun", "Marche"],
        "count": [32, 28, 21, 15, 8]
    })

# Leaderboard
def get_leaderboard(company_id):
    teams = ["Équipe IT", "Équipe Marketing", "Équipe RH", "Équipe Commercial", "Équipe Ops"]
    data = []
    for i, team in enumerate(teams):
        data.append({
            "rank": i + 1,
            "team_name": team,
            "total_points": random.randint(200, 500),
            "co2_saved_kg": round(random.uniform(30, 100), 1),
            "members_count": random.randint(5, 12),
        })
    return pd.DataFrame(data).sort_values("total_points", ascending=False).reset_index(drop=True)

