import streamlit as st
import pandas as pd
import random
from data.mock_data import COMPANIES, SITES, get_rse_metrics

st.set_page_config(page_title="Predict'Mob - Back-office Entreprise", page_icon="🚆", layout="wide")

# État de session pour l'onboarding
if "onboarding_done" not in st.session_state:
    st.session_state.onboarding_done = False
if "current_company" not in st.session_state:
    st.session_state.current_company = None

# Fonction pour simuler la lecture du fichier Excel
def process_employee_file(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        # Vérifier les colonnes nécessaires
        required_cols = ["email", "code_postal_domicile"]
        if not all(col in df.columns for col in required_cols):
            return None, f"❌ Colonnes manquantes. Attendu : {required_cols}"
        return df, None
    except Exception as e:
        return None, f"❌ Erreur de lecture : {str(e)}"

# === PAGE ONBOARDING ===
if not st.session_state.onboarding_done:
    st.title("🚀 Onboarding Entreprise - Predict'Mob")
    st.markdown("Bienvenue ! Configurons votre espace en quelques étapes.")
    
    # Template Excel en dehors du formulaire
    st.subheader("👥 Étape préliminaire : Préparez votre fichier Excel")
    st.markdown("""
    **Format Excel attendu** (colonnes obligatoires) :
    - `email` : adresse email du salarié
    - `code_postal_domicile` : code postal du domicile
    - `gare_depart` (optionnel) : gare habituelle de départ
    """)
    
    # Créer un template Excel exemple
    template_df = pd.DataFrame({
        "email": ["employe1@example.com", "employe2@example.com", "employe3@example.com"],
        "code_postal_domicile": ["75001", "92400", "91190"],
        "gare_depart": ["Gare de Lyon", "La Défense", "Massy-Palaiseau"]
    })
    
    # Convertir en bytes pour le bouton de téléchargement
    from io import BytesIO
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        template_df.to_excel(writer, index=False)
    
    st.download_button(
        label="📥 Télécharger le template Excel",
        data=buffer.getvalue(),
        file_name="template_salaries_predictmob.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="Téléchargez ce template, remplissez-le avec vos données, puis importez-le ci-dessous"
    )
    
    st.divider()
    
    # Formulaire d'onboarding
    with st.form("onboarding_form"):
        st.subheader("📋 Étape 1 : Informations entreprise")
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Nom de l'entreprise *", placeholder="Ex: Acme Corp")
            company_siren = st.text_input("SIREN *", placeholder="123456789", max_chars=9, help="9 chiffres")
        with col2:
            company_sector = st.selectbox("Secteur d'activité *", 
                ["Tech", "Finance", "Environnement", "Industrie", "Services", "Autre"])
        
        st.subheader("🏢 Étape 2 : Site principal")
        site_name = st.text_input("Nom du site", placeholder="Ex: Siège Paris")
        site_address = st.text_area("Adresse", placeholder="10 rue de Rivoli, 75001 Paris", height=80)
        
        st.subheader("👥 Étape 3 : Import des salariés")
        uploaded_file = st.file_uploader(
            "📤 Importer le fichier Excel des salariés", 
            type=["xlsx", "xls"],
            help="Utilisez le template téléchargé ci-dessus"
        )
        
        st.info("💡 Tous les champs marqués d'un * sont obligatoires")
        
        # Boutons du formulaire
        col1, col2 = st.columns([3, 1])
        with col1:
            submit_button = st.form_submit_button("✅ Valider et créer l'espace entreprise", use_container_width=True)
        with col2:
            skip_button = st.form_submit_button("⏭️ Passer (démo)", use_container_width=True)
        
        if skip_button:
            # Mode démo sans onboarding complet
            st.session_state.onboarding_done = True
            st.session_state.current_company_id = 1
            st.rerun()
        
        if submit_button:
            # Validation basique
            if not company_name or not company_siren:
                st.error("❌ Veuillez remplir au minimum le nom et le SIREN de l'entreprise.")
            elif len(company_siren) != 9 or not company_siren.isdigit():
                st.error("❌ Le SIREN doit contenir exactement 9 chiffres.")
            elif uploaded_file is None:
                st.warning("⚠️ Aucun fichier importé. Vous pourrez ajouter des salariés plus tard.")
                # Finaliser sans fichier
                st.session_state.onboarding_done = True
                st.session_state.current_company = {
                    "name": company_name,
                    "siren": company_siren,
                    "sector": company_sector,
                    "nb_employees": 0
                }
                st.session_state.current_company_id = 1
                st.success("✅ Entreprise créée ! Redirection vers le dashboard...")
                st.balloons()
                st.rerun()
            else:
                # Traiter le fichier Excel
                df, error = process_employee_file(uploaded_file)
                if error:
                    st.error(error)
                else:
                    st.success(f"✅ Onboarding terminé ! {len(df)} salariés importés.")
                    st.info(f"""
                    **Prochaines étapes :**
                    - ✉️ Les salariés vont recevoir un email d'invitation
                    - 📱 Ils pourront activer l'option "Partager mes mobilités" dans l'app mobile
                    - 📊 Leurs données apparaîtront dans le dashboard RSE une fois le partage activé
                    """)
                    
                    # Aperçu des données importées
                    with st.expander("👀 Aperçu des salariés importés"):
                        st.dataframe(df.head(10), use_container_width=True)
                    
                    # Finaliser l'onboarding
                    st.session_state.onboarding_done = True
                    st.session_state.current_company = {
                        "name": company_name,
                        "siren": company_siren,
                        "sector": company_sector,
                        "nb_employees": len(df)
                    }
                    st.session_state.current_company_id = 1
                    st.balloons()
                    st.rerun()

# === PAGE DASHBOARD (après onboarding) ===
else:
    # Sidebar
    with st.sidebar:
        st.title("🚆 Predict'Mob")
        st.markdown("**Back-office Entreprise**")
        st.divider()
        
        # Sélection entreprise (mock)
        company = st.selectbox(
            "Entreprise",
            options=[c["id"] for c in COMPANIES],
            format_func=lambda x: next(c["name"] for c in COMPANIES if c["id"] == x)
        )
        st.session_state.current_company_id = company
        
        st.divider()
        
        # Bouton pour refaire l'onboarding
        if st.button("🔄 Nouvelle entreprise"):
            st.session_state.onboarding_done = False
            st.rerun()
        
        st.divider()
        st.caption("Hackathon Mobilités 2025")
        st.caption("Équipe Predict'Mob")
    
    # Page d'accueil
    st.title("🏠 Tableau de Bord Entreprise")
    
    company_data = next(c for c in COMPANIES if c["id"] == st.session_state.current_company_id)
    st.markdown(f"### {company_data['name']} ({company_data['sector']})")
    
    # Récupérer les métriques
    metrics = get_rse_metrics(st.session_state.current_company_id)
    
    # Afficher les KPIs
    st.subheader("📊 Métriques RSE du mois")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🌱 CO₂ évité",
            value=f"{metrics['co2_saved_kg']} kg",
            delta="+12% vs mois dernier"
        )
    
    with col2:
        participation_rate = round(metrics['nb_participants'] / metrics['total_employees'] * 100, 1)
        st.metric(
            label="👥 Salariés participants",
            value=f"{metrics['nb_participants']}/{metrics['total_employees']}",
            delta=f"{participation_rate}%"
        )
    
    with col3:
        st.metric(
            label="🚗 Taux covoiturage",
            value=f"{metrics['covoiturage_rate']*100:.0f}%",
            delta="+5%"
        )
    
    with col4:
        st.metric(
            label="🚴 Trajets durables",
            value=metrics['nb_trajets_durables'],
            delta=f"+{random.randint(5, 15)}"
        )
    
    st.divider()
    
    # Liens rapides
    st.subheader("🔗 Accès rapides")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 Voir le Dashboard RSE complet", use_container_width=True):
            st.switch_page("pages/1_📊_Dashboard_RSE.py")
    
    with col2:
        if st.button("⚠️ Voir les Hotspots", use_container_width=True):
            st.switch_page("pages/2_⚠️_Hotspots.py")
    
    with col3:
        if st.button("🏆 Voir le Leaderboard", use_container_width=True):
            st.switch_page("pages/3_🏆_Leaderboard.py")
    
    # Informations supplémentaires
    st.divider()
    with st.expander("ℹ️ Comment ça marche ?"):
        st.markdown("""
        **Predict'Mob** vous aide à :
        1. 📊 **Suivre les mobilités durables** de vos salariés (avec leur consentement)
        2. ⚠️ **Anticiper les perturbations** train/RER et proposer des alternatives
        3. 🏆 **Gamifier** l'engagement avec des points et badges
        4. 📥 **Générer des rapports RSE** pour vos bilans carbone
        
        **Privacy by design** : Seuls les salariés ayant activé l'option "Partager mes mobilités" 
        contribuent aux métriques de l'entreprise.
        """)

