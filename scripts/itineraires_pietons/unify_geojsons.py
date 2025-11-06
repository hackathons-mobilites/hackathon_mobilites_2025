import json
from pathlib import Path

# Dossier contenant les fichiers GeoJSON d'itinéraires piétons vers POI
INPUT_FOLDER = Path("data/output_SQY")
OUTPUT_FILE = Path("data/geojson_SQY_itineraires_pietons_agrege.geojson")

# Initialisation de la FeatureCollection finale
aggregated = {"type": "FeatureCollection", "features": []}

# Parcours des fichiers .geojson
all_geojson_files = list(INPUT_FOLDER.glob("*.geojson"))
print(f"Found {len(all_geojson_files)} GeoJSON files in {INPUT_FOLDER}")

for file in INPUT_FOLDER.glob("*.geojson"):
    with open(file, encoding="utf-8") as f:
        data = json.load(f)

        for feature in data.get("features", []):
            # Les propriétés sont déjà complètes dans ces fichiers
            # On peut ajouter le nom du fichier source si besoin
            feature["properties"]["fichier_source"] = file.name
            aggregated["features"].append(feature)

# Écriture dans un nouveau fichier GeoJSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
    json.dump(aggregated, f_out, ensure_ascii=False, indent=2)

print(f"Agrégation terminée : {OUTPUT_FILE}")
print(f"Total features agrégées : {len(aggregated['features'])}")

# Affichage d'un échantillon des propriétés disponibles
if aggregated["features"]:
    print("\nPropriétés disponibles dans les features :")
    sample_props = aggregated["features"][0]["properties"]
    for key in sample_props.keys():
        print(f"  - {key}: {sample_props[key]}")