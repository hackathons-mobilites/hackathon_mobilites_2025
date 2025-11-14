import pandas as pd

LIGNE_U_STATION_ORDER = [
    "LA-DEFENSE",
    "PUTEAUX",
    "SURESNES-MONT-VALERIEN",
    "SAINT-CLOUD",
    "SEVRES-VILLE-D'AVRAY",
    "CHAVILLE-RIVE-DROITE",
    "VERSAILLES-CHANTIERS",
    "SAINT-CYR",
    "SAINT-QUENTIN-EN-YVELINES-MONTIGNY-LE-BRETONNEUX",
    "TRAPPES",
    "LA-VERRIERE",
]

LIGNE_L_STATION_ORDER = [
    "PARIS-SAINT-LAZARE",
    "HAUSSMANN-SAINT-LAZARE",
    "MADELEINE",
]

LIGNE_ORDER = {
    "U": LIGNE_U_STATION_ORDER,
    "L": LIGNE_L_STATION_ORDER,
}

LINE_LOOKUPS_INDEX = {
    line: {station: idx for idx, station in enumerate(stations)}
    for line, stations in LIGNE_ORDER.items()
}


def map_gare_to_index_in_line(row: pd.Series, gare_column_name: str = "Gare") -> int:
    gare = row.get(gare_column_name)
    ligne = row.get("Ligne")

    if pd.isna(gare) or pd.isna(ligne):
        return -1

    key = str(gare).strip()
    line_key = str(ligne).strip()

    lookup = LINE_LOOKUPS_INDEX.get(line_key)
    if lookup is None:
        return -1

    return lookup.get(key, -1)
