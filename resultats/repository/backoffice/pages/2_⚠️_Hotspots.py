import streamlit as st
import pandas as pd
import sys
sys.path.append('..')
from data.mock_data import HOTSPOTS

st.set_page_config(page_title="Hotspots", page_icon="⚠️", layout="wide")

st.title("⚠️ Hotspots en Temps Réel")
st.markdown("Zones/gares à risque affectant vos salariés")

st.info("💡 Les hotspots sont détectés automatiquement par notre moteur IA en analysant les prédictions de retard et les trajets de vos salariés.")

st.divider()

# Afficher les hotspots
for hotspot in HOTSPOTS:
    severity_color = {"high": "🔴", "medium": "🟠", "low": "🟡"}
    severity_label = {"high": "Élevé", "medium": "Moyen", "low": "Faible"}
    
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            st.markdown(f"### {severity_color[hotspot['risk_level']]} {hotspot['gare_name']}")
            st.caption(f"Niveau de risque : {severity_label[hotspot['risk_level']]}")
        
        with col2:
            st.metric("Salariés impactés", hotspot['nb_trajets_affectes'])
        
        with col3:
            st.write(f"🕐 Heure de pointe : **{hotspot['datetime_debut'].strftime('%H:%M')}**")
        
        with col4:
            if st.button("📋 Détails", key=f"hotspot_{hotspot['id']}", use_container_width=True):
                st.info(f"Alternatives proposées pour ce hotspot (fonctionnalité à implémenter)")
        
        st.divider()

# Statistiques globales
st.subheader("📊 Statistiques des hotspots")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total hotspots actifs", len(HOTSPOTS))

with col2:
    total_impacted = sum(h['nb_trajets_affectes'] for h in HOTSPOTS)
    st.metric("Total salariés impactés", total_impacted)

with col3:
    high_risk_count = len([h for h in HOTSPOTS if h['risk_level'] == 'high'])
    st.metric("Hotspots critiques", high_risk_count)

