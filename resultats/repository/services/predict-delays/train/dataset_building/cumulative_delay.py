import pandas as pd


def compute_cumulative_delay_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """Return expanded rows for each (departure stop i, arrival stop j>i).

    Output columns: ['Ligne','Gare_depart','Terminus','Gare_arrival','number_of_stops',
                     'additional_delays','final_delay_at_arrival']

    number_of_stops is computed as (Gare_index_arrival - Gare_index_depart).
    additional_delays is computed as (delay at arrival) - (delay at departure),
    where delays are taken from the 'Delais_départ' column (missing values treated as 0.0).
    final_delay_at_arrival is simply the delay value at the arrival station.
    """

    required = {"Ligne", "Gare_index", "Delais_départ"}
    if not required.issubset(df.columns):
        raise ValueError(f"DataFrame must contain columns: {required}")

    working = df.copy()
    working["_delay_fill"] = working["Delais_départ"].fillna(0.0).astype(float)

    rows = []

    def _process_group(g: pd.DataFrame):
        # sort by station index
        g_sorted = (
            g.dropna(subset=["Gare_index"])
            .sort_values("Gare_index")
            .reset_index(drop=False)
        )
        if g_sorted.shape[0] <= 1:
            return

        indices = g_sorted["Gare_index"].to_numpy()

        for i in range(len(g_sorted)):
            for j in range(i + 1, len(g_sorted)):
                # compute additional delay as arrival_delay - departure_delay
                arrival_delay = float(g_sorted["_delay_fill"].iat[j])
                depart_delay = float(g_sorted["_delay_fill"].iat[i])
                additional = arrival_delay - depart_delay

                row = {
                    "Ligne": g_sorted.iloc[i]["Ligne"],
                    "DateTemps_gare_depart": g_sorted.iloc[i]["DateTemps"],
                    "Gare_depart": g_sorted.iloc[i]["Gare"],
                    "Gare_depart_index": g_sorted.iloc[i]["Gare_index"],
                    "Direction": g_sorted.iloc[i]["Direction"],
                    "Terminus": g_sorted.iloc[i]["Terminus"],
                    "Gare_arrivee": g_sorted.iloc[j]["Gare"],
                    "Gare_arrivee_index": g_sorted.iloc[j]["Gare_index"],
                    "Nombre_arret": abs(int(indices[j] - indices[i]))
                    if pd.notna(indices[j]) and pd.notna(indices[i])
                    else pd.NA,
                    "Retard_additionnel_a_l_arrivee": float(additional),
                    "Retard_a_gare_d_arrivee": float(arrival_delay),
                    "Taux_occupation_total": float(g_sorted.iloc[i]["Taux_occupation"]),
                    "Trajet_id": g_sorted.iloc[i]["trip_id"],
                }
                rows.append(row)

    # group by line and trip_id so we generate pairs per trip (DateTemps is too granular)
    group_keys = ["Ligne", "trip_id"]
    # iterate groups explicitly to avoid type-checker issues with groupby.apply
    for _gk, group in working.groupby(group_keys, dropna=False, group_keys=False):
        _process_group(group)

    if not rows:
        return pd.DataFrame(
            columns=[
                "Ligne",
                "Gare_depart",
                "Terminus",
                "Gare_arrival",
                "number_of_stops",
                "additional_delays",
                "final_delay_at_arrival",
                "trip_id",
            ]
        )

    return pd.DataFrame(rows)
