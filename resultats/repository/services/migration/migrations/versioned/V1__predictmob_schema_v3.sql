
-- Schema PostgreSQL pour Predict'Mob v3 (double levier)

CREATE TABLE companies (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    siren           VARCHAR(9),
    sector          TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE company_sites (
    id              SERIAL PRIMARY KEY,
    company_id      INT REFERENCES companies(id),
    name            TEXT NOT NULL,
    address         TEXT,
    lat             DOUBLE PRECISION,
    lon             DOUBLE PRECISION,
    insee_code      VARCHAR(10),
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE employees (
    id              SERIAL PRIMARY KEY,
    company_id      INT REFERENCES companies(id),
    email_hash      TEXT NOT NULL,
    home_postcode   VARCHAR(10),
    home_lat        DOUBLE PRECISION,
    home_lon        DOUBLE PRECISION,
    default_site_id INT REFERENCES company_sites(id),
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE employee_settings (
    employee_id         INT PRIMARY KEY REFERENCES employees(id),
    share_enabled       BOOLEAN DEFAULT false,
    updated_at          TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE trajectories (
    id                  SERIAL PRIMARY KEY,
    employee_id         INT REFERENCES employees(id),
    gare_depart_code    TEXT NOT NULL,
    gare_depart_name    TEXT,
    gare_arrivee_code   TEXT NOT NULL,
    gare_arrivee_name   TEXT,
    usual_departure_time TIME,
    created_at          TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE predictions (
    id                  SERIAL PRIMARY KEY,
    trajectory_id       INT REFERENCES trajectories(id),
    gare_risque_code    TEXT NOT NULL,
    gare_risque_name    TEXT,
    forecast_datetime   TIMESTAMPTZ NOT NULL,
    prob_retard         DOUBLE PRECISION NOT NULL,
    model_version       TEXT,
    created_at          TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_predictions_gare_time
    ON predictions (gare_risque_code, forecast_datetime);

CREATE TABLE hotspots (
    id                      SERIAL PRIMARY KEY,
    gare_code               TEXT NOT NULL,
    gare_name               TEXT,
    datetime_debut          TIMESTAMPTZ NOT NULL,
    datetime_fin            TIMESTAMPTZ NOT NULL,
    nb_trajets_affectes     INT NOT NULL,
    prob_retard_max         DOUBLE PRECISION NOT NULL,
    prob_retard_moyenne     DOUBLE PRECISION,
    risk_level              TEXT NOT NULL,
    created_at              TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_hotspots_gare_time
    ON hotspots (gare_code, datetime_debut);

CREATE TABLE alternatives (
    id                  SERIAL PRIMARY KEY,
    hotspot_id          INT REFERENCES hotspots(id),
    type                TEXT NOT NULL,
    offre               TEXT NOT NULL,
    partenaire          TEXT,
    places_disponibles  INT,
    deeplink            TEXT,
    score_rse           DOUBLE PRECISION,
    created_at          TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_alternatives_hotspot
    ON alternatives (hotspot_id, type);

CREATE TABLE mobility_events (
    id                  SERIAL PRIMARY KEY,
    employee_id         INT REFERENCES employees(id),
    event_datetime      TIMESTAMPTZ NOT NULL,
    mode                TEXT NOT NULL, -- train, velo, covoit, marche, etc.
    co2_saved_kg        DOUBLE PRECISION,
    shared_with_company BOOLEAN DEFAULT false,
    created_at          TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE commute_logs (
    id                  SERIAL PRIMARY KEY,
    employee_id         INT REFERENCES employees(id),
    trajectory_id       INT REFERENCES trajectories(id),
    hotspot_id          INT REFERENCES hotspots(id),
    alternative_id      INT REFERENCES alternatives(id),
    date_trajet         DATE NOT NULL,
    mode_final          TEXT,
    co2_saved_kg        DOUBLE PRECISION,
    created_at          TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE rewards (
    id                  SERIAL PRIMARY KEY,
    employee_id         INT REFERENCES employees(id),
    type                TEXT NOT NULL, -- 'badge' ou 'points'
    label               TEXT NOT NULL,
    points              INT DEFAULT 0,
    period              TEXT,
    created_at          TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE employee_points (
    id                  SERIAL PRIMARY KEY,
    employee_id         INT REFERENCES employees(id),
    period              TEXT NOT NULL,
    points_total        INT DEFAULT 0,
    updated_at          TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE company_rse_snapshot (
    id                      SERIAL PRIMARY KEY,
    company_id              INT REFERENCES companies(id),
    period                  TEXT NOT NULL,
    co2_total_saved_kg      DOUBLE PRECISION,
    nb_trajets_partages     INT,
    nb_trajets_durables     INT,
    covoiturage_rate        DOUBLE PRECISION,
    created_at              TIMESTAMPTZ DEFAULT now()
);
