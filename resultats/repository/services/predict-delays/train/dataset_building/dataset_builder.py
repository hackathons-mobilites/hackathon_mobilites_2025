from datetime import datetime
from pathlib import Path

import pandas as pd
from cumulative_delay import compute_cumulative_delay_pairs


def build_full_trip_dataset():
    """Builds the trip dataset for training the delays prediction model."""
    raw_df = read_raw_dataset()
    processed_df = compute_delays(raw_df)
    processed_df = compute_full_date(processed_df)
    processed_df = compute_gare_index(processed_df)
    processed_df = compute_terminus_index(processed_df)
    processed_df = compute_direction_columns(processed_df)
    processed_df = compute_trip_id(processed_df)
    processed_df = drop_unused_columns(processed_df)
    processed_df.dropna(inplace=True)

    processed_df = compute_cumulative_delay_pairs(processed_df)

    return processed_df


def read_raw_dataset():
    """Builds the dataset for training the delays prediction model."""
    dataset_dtype = {
        "Ligne": "category",
        "Gare": "category",
        "Terminus": "category",
    }
    parse_dates = [
        "Date",
        "Heure_départ_théorique",
        "Heure_départ_réalisé",
    ]
    converters = {
        "Taux_occupation_total": lambda x: x.replace(",", ".")
        if isinstance(x, str)
        else x
    }
    usecols = list(dataset_dtype.keys()) + parse_dates

    dataset_path_list = Path(".").glob("*.csv")
    dataset_list = [
        pd.read_csv(
            path,
            dtype=dataset_dtype,  # type: ignore
            parse_dates=parse_dates,
            converters=converters,
            usecols=usecols,
        )
        for path in dataset_path_list
    ]
    concatenated_df = pd.concat(dataset_list, ignore_index=True)

    return concatenated_df


def compute_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Builds the dataset for training the delays prediction model."""
    df["Delais_départ"] = (
        df["Heure_départ_réalisé"] - df["Heure_départ_théorique"]
    ).dt.total_seconds()

    df = df.dropna(subset=["Delais_départ"])

    return df


def compute_full_date(df: pd.DataFrame) -> pd.DataFrame:
    """Combine 'Date' and time columns into full datetime columns."""
    df.loc[:, "DateTemps"] = df.apply(
        lambda row: datetime.combine(
            row["Date"].date(), row["Heure_départ_théorique"].time()
        ),
        axis=1,
    )

    return df


def drop_unused_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drops unused columns from the dataset."""
    columns_to_drop = [
        "Heure_départ_théorique",
        "Heure_départ_réalisé",
        "Date",
    ]
    df = df.drop(columns=columns_to_drop)

    return df


def compute_gare_index(df: pd.DataFrame) -> pd.DataFrame:
    """Map each `Gare` value to its index depending on the `Ligne` value.

    Uses `LIGNE_U_STATION_ORDER` when `Ligne == 'U'` and
    `LIGNE_L_STATION_ORDER` when `Ligne == 'L'.

    If a station or line is not found, the index will be set to -1.
    """
    # Use a relative import when the package context is available (normal package import).
    # Fall back to an absolute import when running as a script or from a notebook where
    # there is no parent package (avoids "attempted relative import with no known parent package").
    from station_order import map_gare_to_index_in_line

    df.loc[:, "Gare_index"] = df.apply(
        map_gare_to_index_in_line, gare_column_name="Gare", axis=1
    )

    return df


def compute_terminus_index(df: pd.DataFrame) -> pd.DataFrame:
    """Map each `Terminus` value to its index depending on the `Ligne` value.

    Uses `LIGNE_U_STATION_ORDER` when `Ligne == 'U'` and
    `LIGNE_L_STATION_ORDER` when `Ligne == 'L'.

    If a station or line is not found, the index will be set to -1.
    """
    from station_order import map_gare_to_index_in_line

    df.loc[:, "Terminus_index"] = df.apply(
        map_gare_to_index_in_line, gare_column_name="Terminus", axis=1
    )

    return df


def compute_trip_id(df: pd.DataFrame) -> pd.DataFrame:
    """Assign a `trip_id` to rows that belong to the same train trip.

    A trip is a sequence of rows for the same train (same `Ligne` and `Terminus`),
    where consecutive station indexes are adjacent (difference of 1) and the
    timestamps (`DateTemps`) are monotonic with the station index (increasing
    or decreasing consistently).

    The function preserves the existing row order and returns a new column
    `trip_id` which is an integer starting at 0 for the first identified trip
    and growing.
    """
    # Work on a copy and ensure we have the columns we need
    required_cols = ["Ligne", "Terminus", "Gare_index", "DateTemps"]
    for c in required_cols:
        if c not in df.columns:
            raise KeyError(f"Required column '{c}' not found in DataFrame")

    # Keep original index so we can restore order later.
    temp = df.reset_index().rename(columns={"index": "orig_index"})

    # We'll group by Ligne + Terminus and scan each group to create trip ids
    temp["trip_id"] = -1

    current_trip = 0

    group_cols = ["Ligne", "Terminus"]
    for _, group in temp.groupby(group_cols, sort=False, observed=True):
        # sort group by DateTemps to scan in time order
        g = group.sort_values("DateTemps").copy()

        # prepare an array to fill trip ids for this group's rows (indexed by g.index)
        trip_ids: list[int | None] = [-1] * len(g)

        group_trip_id = None
        prev_station = None
        prev_time = None
        direction = None

        for pos, (_, row) in enumerate(g.iterrows()):
            gare = int(row["Gare_index"]) if pd.notna(row["Gare_index"]) else None
            time = row["DateTemps"]

            if gare is None or pd.isna(time):
                # cannot include in a trip
                group_trip_id = None
                prev_station = None
                prev_time = None
                direction = None
                trip_ids[pos] = -1
                continue

            if prev_station is None:
                # start a new trip for this group
                group_trip_id = current_trip
                trip_ids[pos] = group_trip_id
                current_trip += 1
                prev_station = gare
                prev_time = time
                direction = None
                continue

            # stations must be adjacent
            if abs(gare - prev_station) != 1:
                # start a new trip
                group_trip_id = current_trip
                trip_ids[pos] = group_trip_id
                current_trip += 1
                prev_station = gare
                prev_time = time
                direction = None
                continue

            # determine direction if unknown
            if direction is None:
                if time > prev_time:
                    direction = 1
                elif time < prev_time:
                    direction = -1
                else:
                    # ambiguous timestamp, start new trip
                    group_trip_id = current_trip
                    trip_ids[pos] = group_trip_id
                    current_trip += 1
                    prev_station = gare
                    prev_time = time
                    direction = None
                    continue

                # continue same trip
                trip_ids[pos] = group_trip_id
                prev_station = gare
                prev_time = time
                continue

            # check monotonicity
            if (direction == 1 and time >= prev_time) or (
                direction == -1 and time <= prev_time
            ):
                trip_ids[pos] = group_trip_id
                prev_station = gare
                prev_time = time
                continue
            else:
                # monotonicity broken — start a new trip
                group_trip_id = current_trip
                trip_ids[pos] = group_trip_id
                current_trip += 1
                prev_station = gare
                prev_time = time
                direction = None

        # assign the computed trip ids back to temp using the original indices
        trip_series = pd.Series(trip_ids, index=g.index)
        temp.loc[trip_series.index, "trip_id"] = trip_series

    # restore original order
    temp = temp.sort_values("orig_index")

    # merge trip_id back into original dataframe (align by original index)
    df = df.copy()
    df["trip_id"] = temp.set_index("orig_index")["trip_id"]

    return df


def compute_direction_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Compute direction columns based on `Gare_index` and `Terminus_index`.

    Adds a new column `direction` which is:
    - 1 if the train is moving towards increasing station indexes
    - -1 if the train is moving towards decreasing station indexes
    """

    df.loc[:, "Direction"] = (df["Terminus_index"] > 0) * 2 - 1

    return df
