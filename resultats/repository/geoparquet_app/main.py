import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import geopandas as gpd

p = Path(__file__).parent
p = p. parent.parent.parent

color_map = {
    'Etablissements adultes handicapés': '#FFC0CB',  # Light Pink
    'Etablissements enfants handicapés': "#88F3E5",  # Light Coral
    'Etablissements hospitaliers': "#96FD96"         # Peach Puff
}



# Set page config
st.set_page_config(layout="wide")

st.title("🍕 Reg'inna Carte d'acces mobilité 🗺️")

# --- 1. Data Caching for Performance ---
# Use st.cache_data to load or generate data once.
# This is the single most important optimization.
@st.cache_data
def load_data():
    """Generates a sample DataFrame for the map."""
    # Create sample data (replace with your actual data loading)

    PARQUET_FILE = p / "data/enrich/final_table.gpq"
    # np.random.seed(42)
    # data = {
    #     'Lat': 34 + np.random.randn(1000) * 5,  # Sample latitudes
    #     'Lon': -100 + np.random.randn(1000) * 5, # Sample longitudes
    #     'Magnitude': np.random.randint(1, 10, 1000),
    #     'City': [f'Location {i}' for i in range(1000)]
    # }
    # df = pd.DataFrame(data)
    df = gpd.read_parquet(PARQUET_FILE)
    df["Lon"] = df.geometry.x
    df["Lat"] = df.geometry.y

    PARQUET_ET = p / "data/interim/etablissements.gpq"  # Corrected file path

    # Ensure the path is resolved correctly
    if not PARQUET_ET.exists():
        raise FileNotFoundError(f"The file {PARQUET_ET} does not exist.")

    dfe = gpd.read_parquet(PARQUET_ET)
    dfe["Lon"] = dfe.geometry.x
    dfe["Lat"] = dfe.geometry.y

    dfe["color_code"] = dfe["type_etablissement"].map(color_map)

    return df, dfe 

df, dfe = load_data()

# --- 2. Map Generation ---
def create_map(dataframe, dataframe_e, color_col):
    """Creates the Plotly Express Mapbox figure."""

    
    fig = px.scatter_mapbox(
        dataframe,
        lat="Lat",
        lon="Lon",
        color=color_col,
        # hover_name="City",
        # size="Magnitude",
        color_continuous_scale=px.colors.cyclical.IceFire,
        zoom=10,
        height=600
    )

    fig.add_trace(
        go.Scattermapbox(
        lat=dataframe_e['Lat'],
        lon=dataframe_e['Lon'],
        mode='markers',
        marker = go.scattermapbox.Marker( 
            size=7,
            color="black", 
            # 🎯 MODIFICATION HERE: Set the marker symbol to 'square' 🎯
        ),
        name='Source 2: Etablissement (Edge)',
        text=dataframe_e['raison_social'],
        hoverinfo='text'
        )
    )

    fig.add_trace(
        go.Scattermapbox(
        lat=dataframe_e['Lat'],
        lon=dataframe_e['Lon'],
        mode='markers',
        marker = go.scattermapbox.Marker( 
            size=5,
            color=dataframe_e['color_code'], 
            # 🎯 MODIFICATION HERE: Set the marker symbol to 'square' 🎯
        ),
        name='Source 2: Etablissement',
        text=dataframe_e['raison_social'],
        hoverinfo='text'
        )
    )
    
    # Optional: Customize map style (requires a Mapbox token for some styles)
    # Using a free public style:
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    
    return fig

# --- 3. Streamlit App Layout ---
# Example of a user control that triggers a map update
color_option = st.selectbox(
    'Select column to color points by:',
    ('facilite_acces_code')
)


if __name__ == "__main__":
    # Render the Plotly chart
    fig = create_map(df,dfe,  color_option)
    st.plotly_chart(fig, use_container_width=True)