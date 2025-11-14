from typing import List

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import (
    FunctionTransformer,
    MinMaxScaler,
    OneHotEncoder,
    PolynomialFeatures,
    SplineTransformer,
    StandardScaler,
)
from xgboost import XGBRegressor

# dataset schema (kept for reference)
dataset_schema = {
    "Ligne": "category",  # nom de la ligne de train
    "DateTemps_gare_depart": "datetime",  # date et heure de départ de la gare
    "Gare_depart_index": "float",  # index de la gare de départ dans la ligne
    "Gare_arrivee_index": "float",  # index de la gare d'arrivée dans la ligne
    "Direction": "int8",  # 1 if the train is moving towards increasing station indexes, -1 otherwise
    "Nombre_arret": "float",  # nombre d'arrêts entre la gare de départ et la gare d'arrivée
    "Taux_occupation_total": "float32",  # taux d'occupation total du train en pourcentage
    "Delais_additionnel_a_l_arrivee": "float",  # retard additionnel du train à l'arrivée en secondes par rapport au depart
    "Retard_a_gare_d_arrivee": "float",  # retard du train à l'arrivée en secondes par aux horaires prévus
    # Les phenomenes vont de 1 à 4 pour indiquer leur intensité
    "phenomene_1": "int8",  # vent
    "phenomene_2": "int8",  # pluie
    "phenomene_3": "int8",  # orages
    "phenomene_4": "int8",  # crues
    "phenomene_5": "int8",  # neige / verglas
    "phenomene_6": "int8",  # canicule
    "phenomene_7": "int8",  # grand froid
    "temperature_instant": "int32",  # température instantanée en degrés Celsius
    "quantite_precipitations": "float32",  # quantité de précipitations en mm
}


TARGET_COLUMN = "Delais_additionnel_a_l_arrivee"
DROP_COLUMN = "Retard_a_gare_d_arrivee"


# Small helpers ---------------------------------------------------------------
def select_columns(cols: List[str]):
    """Return a FunctionTransformer that selects DataFrame columns by name."""

    return FunctionTransformer(lambda X: X[cols], validate=False)


def datetime_to_timestamp_seconds(X):
    """Convert a single-column DataFrame/array with datetimes to a (n_samples,1) float array of seconds since epoch."""
    # accept DataFrame or array-like
    s = pd.to_datetime(pd.Series(X.ravel()))
    return (s.astype("int64") / 1e9).to_numpy().reshape(-1, 1)


def datetime_to_workingday(X):
    """Return a (n_samples, 1) array with 1 for working day (Mon-Fri) else 0.

    Expects a single-column DataFrame/array of datetimes or strings.
    """
    s = pd.to_datetime(pd.Series(X.ravel()))
    # pandas weekday: Monday=0 .. Sunday=6
    is_working = s.dt.weekday < 5
    return is_working.astype(int).to_numpy().reshape(-1, 1)


# Build pipelines -------------------------------------------------------------
# Date pipeline: extract timestamp then spline transform


def periodic_spline_transformer(period, n_splines=None, degree=3):
    if n_splines is None:
        n_splines = period
    n_knots = n_splines + 1  # periodic and include_bias is True
    return SplineTransformer(
        degree=degree,
        n_knots=n_knots,
        knots=np.linspace(0, period, n_knots).reshape(n_knots, 1),
        extrapolation="periodic",
        include_bias=True,
    )


date_pipeline = Pipeline(
    [
        ("working_day", FunctionTransformer(datetime_to_workingday, validate=False)),
        ("cyclic_month", periodic_spline_transformer(12, n_splines=6), ["month"]),
        ("cyclic_weekday", periodic_spline_transformer(7, n_splines=3), ["weekday"]),
        ("cyclic_hour", periodic_spline_transformer(24, n_splines=12), ["hour"]),
    ]
)

# Phenomena pipeline: keep phenomene_1 and phenomene_3 and add their interaction
phen_cols = ["phenomene_1", "phenomene_3"]

# poly pipeline that returns only the interaction term x1*x2
poly_interaction_only = Pipeline(
    [
        (
            "poly",
            PolynomialFeatures(degree=2, interaction_only=True, include_bias=False),
        ),
        (
            "select_interaction",
            FunctionTransformer(lambda X: X[:, -1].reshape(-1, 1), validate=False),
        ),
    ]
)

# combine originals + interaction using FeatureUnion
phen_pipeline = (
    FeatureUnion(
        [
            ("original", FunctionTransformer(lambda X: X, validate=False)),
            ("interaction", poly_interaction_only),
        ]
    ),
)


# Numeric columns to scale (exclude phenomene_1 and phenomene_3 because handled above)
numeric_cols = [
    "Gare_depart_index",
    "Gare_arrivee_index",
    "Nombre_arret",
    "Direction",
    "temperature_instant",
    "quantite_precipitations",
    "Taux_occupation_total",
    "phenomene_2",
    "phenomene_4",
    "phenomene_5",
    "phenomene_6",
    "phenomene_7",
]

numeric_pipeline = Pipeline(
    [
        ("select", select_columns(numeric_cols)),
        ("scale", StandardScaler()),
    ]
)


# FeatureUnion for gare indices: keep originals and add min-max scaled versions
gare_index_cols = ["Gare_depart_index", "Gare_arrivee_index"]

gare_index_union = FeatureUnion(
    [
        (
            "original",
            Pipeline(
                [
                    ("select", select_columns(gare_index_cols)),
                ]
            ),
        ),
        (
            "minmax",
            Pipeline(
                [
                    ("select", select_columns(gare_index_cols)),
                    ("minmax", MinMaxScaler()),
                ]
            ),
        ),
    ]
)

# Categorical pipeline for 'Ligne'
categorical_cols = ["Ligne"]
categorical_pipeline = OneHotEncoder(handle_unknown="error")


# Compose feature transformer. We explicitly list columns to include so
# DROP_COLUMN and the TARGET_COLUMN are not used as features.
# Use `gare_index_union` to keep originals and add min-max scaled versions
# for the two gare index columns, then use numeric_pipeline for the remaining
# numeric columns (remove gare indices from that list to avoid duplication).
numeric_cols_no_gare = [c for c in numeric_cols if c not in gare_index_cols]

preprocessor = ColumnTransformer(
    [
        ("date", date_pipeline, ["DateTemps_gare_depart"]),
        ("ligne", categorical_pipeline, categorical_cols),
        ("gare_indices", gare_index_union, gare_index_cols),
        ("numeric", numeric_pipeline, numeric_cols_no_gare),
        ("phenomene_interaction", phen_pipeline, phen_cols),
    ],
    remainder="passthrough",
    sparse_threshold=0,
)


# Final pipeline with XGBoost regressor
modeling_pipeline = Pipeline(
    [
        ("preprocessor", preprocessor),
        (
            "model",
            XGBRegressor(
                objective="reg:squarederror", n_estimators=100, random_state=42
            ),
        ),
    ]
)
