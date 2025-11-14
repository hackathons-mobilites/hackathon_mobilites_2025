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

color_class = {
    "1": "Score E",
    "2": "Score D",
    "3": "Score C",
    "4": "Score B",
    "5": "Score A",         
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

    PARQUET_FILE = p / "data/enrich/final_table_with_class.gbq"
    
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
    df["class_id"] = df['class_id'].astype(int).astype(str).map(color_class)
    # df["class_id_num"] = df['class_id'].astype(int).map({
    #         1: 18,   # biggest
    #         2: 15,
    #         3: 12,
    #         4: 9,
    #         5: 6    # smallest
    #     })
    # df["class_s"] = 2
    # df["class_sym"]= df['class_id'].astype(int).map({
    #     1: "circle",
    #     2: "triangle",
    #     3: "square",
    #     4: "star",
    #     5: "marker",
    # })

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

    priority_colors = [
        "#FF0000",  # 1 - high priority
        "#FF7F00",  # 2 - orange
        "#CABC1D",  # 3 - yellow
        "#7FFF00",  # 4 - yellow-green
        "#00CC00"   # 5 - low priority
    ]

    fig = px.scatter_mapbox(
        dataframe,
        lat="Lat",
        lon="Lon",
        color=color_col,
        # size="class_id_num",
        hover_name="nom_zda",
        # size="Magnitude",
        color_discrete_map={
            "Score E": "#FF0000",
            "Score D": "#FF7F00",
            "Score C": "#CABC1D",
            "Score B": "#7FFF00",
            "Score A": "#00CC00",
        },
        # symbol="class_sym",
        zoom=11,
        height=800
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
    fig.update_layout(mapbox_style="carto-positron",
        title={
        "text": "Carte d'accessibilité",
        "x": 0.5,        # centers the title horizontally
        "xanchor": "center",
        "yanchor": "top"
        },
        margin={"r":0, "t":1, "l":0, "b":0}
    )
    
    return fig

# --- 3. Streamlit App Layout ---
# Example of a user control that triggers a map update
color_option = st.selectbox(
    'Select column to color points by:',
    ('class_id','facilite_acces_code',)
)


if __name__ == "__main__":
    # Render the Plotly chart
    fig = create_map(df,dfe,  color_option)
    st.plotly_chart(fig, use_container_width=True)