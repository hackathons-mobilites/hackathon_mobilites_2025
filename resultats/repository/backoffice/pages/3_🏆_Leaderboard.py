import streamlit as st
import sys
sys.path.append('..')
from data.mock_data import get_leaderboard

st.set_page_config(page_title="Leaderboard", page_icon="🏆", layout="wide")

st.title("🏆 Classement des Équipes")
st.markdown("Encouragez la compétition saine et l'engagement collectif vers des mobilités durables")

st.divider()

df_leaderboard = get_leaderboard(st.session_state.get("current_company_id", 1))

# Afficher le podium
st.subheader("🎖️ Podium du mois")
col1, col2, col3 = st.columns(3)

with col2:
    st.markdown("### 🥇 1ère place")
    team = df_leaderboard.iloc[0]
    st.metric("Points", team["total_points"])
    st.markdown(f"**{team['team_name']}**")
    st.caption(f"💚 {team['co2_saved_kg']} kg CO₂ évité")
    st.caption(f"👥 {team['members_count']} membres")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🥈 2ème place")
    team = df_leaderboard.iloc[1]
    st.metric("Points", team["total_points"])
    st.markdown(f"**{team['team_name']}**")
    st.caption(f"💚 {team['co2_saved_kg']} kg CO₂")
    st.caption(f"👥 {team['members_count']} membres")

with col2:
    # Espace vide pour centrer
    st.write("")

with col3:
    st.markdown("### 🥉 3ème place")
    team = df_leaderboard.iloc[2]
    st.metric("Points", team["total_points"])
    st.markdown(f"**{team['team_name']}**")
    st.caption(f"💚 {team['co2_saved_kg']} kg CO₂")
    st.caption(f"👥 {team['members_count']} membres")

st.divider()

# Tableau complet
st.subheader("📋 Classement complet")
st.dataframe(
    df_leaderboard[["rank", "team_name", "total_points", "co2_saved_kg", "members_count"]],
    column_config={
        "rank": "Rang",
        "team_name": "Équipe",
        "total_points": "Points",
        "co2_saved_kg": "CO₂ évité (kg)",
        "members_count": "Membres"
    },
    hide_index=True,
    use_container_width=True
)

st.divider()

# Informations sur le système de points
with st.expander("ℹ️ Comment fonctionnent les points ?"):
    st.markdown("""
    **Système de points Predict'Mob :**
    
    - 🚴 **+10 points** : Trajet en vélo
    - 🚗 **+5 points** : Covoiturage
    - 🏠 **+3 points** : Télétravail (journée complète)
    - 🚶 **+2 points** : Marche à pied (> 20 min)
    - 🚆 **+1 point** : Utilisation d'une alternative lors d'un hotspot
    
    **Badges spéciaux :**
    - 🏅 Éco-warrior : 20 trajets durables
    - 🎯 Plan B Master : 5 alternatives adoptées
    - 💚 Green Champion : 50 kg CO₂ évité
    """)

