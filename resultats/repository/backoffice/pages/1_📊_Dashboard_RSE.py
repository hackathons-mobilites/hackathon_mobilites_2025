import streamlit as st
import plotly.express as px
import sys
sys.path.append('..')
from data.mock_data import get_rse_metrics, get_co2_evolution, get_mobility_distribution

st.set_page_config(page_title="Dashboard RSE", page_icon="📊", layout="wide")

if "current_company_id" not in st.session_state:
    st.session_state.current_company_id = 1

st.title("📊 Dashboard RSE Détaillé")

# Période
period = st.selectbox("Période", ["Semaine", "Mois", "Trimestre", "Année"], index=1)

# Métriques
metrics = get_rse_metrics(st.session_state.current_company_id)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("CO₂ évité (kg)", metrics['co2_saved_kg'])
with col2:
    st.metric("Trajets partagés", metrics['nb_trajets_partages'])
with col3:
    st.metric("Trajets durables", metrics['nb_trajets_durables'])
with col4:
    st.metric("Participants", f"{metrics['nb_participants']}/{metrics['total_employees']}")

st.divider()

# Graphiques
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Évolution CO₂ évité")
    df_co2 = get_co2_evolution(st.session_state.current_company_id)
    fig = px.line(df_co2, x="date", y="co2_saved_kg", 
                  title="CO₂ économisé par jour (kg)",
                  labels={"co2_saved_kg": "CO₂ (kg)", "date": "Date"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🚗 Répartition des modes")
    df_modes = get_mobility_distribution(st.session_state.current_company_id)
    fig = px.pie(df_modes, names="mode", values="count", 
                 title="Modes de transport utilisés")
    st.plotly_chart(fig, use_container_width=True)

# Export
st.divider()
col1, col2 = st.columns([3, 1])
with col1:
    st.info("💡 Les rapports sont basés uniquement sur les salariés ayant activé le partage de données (RGPD compliant)")
with col2:
    if st.button("📥 Exporter le rapport RSE (PDF)", use_container_width=True):
        st.success("✅ Rapport RSE généré ! (fonctionnalité à implémenter)")

