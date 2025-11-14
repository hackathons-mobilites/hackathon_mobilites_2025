from utils.job_runner import JobRunner
from utils.loader_local import LoaderLocal
from utils.writer_local import WriterLocal
import pandas as pd
from math import radians, sin, cos, sqrt, atan2


class EnrichJob(JobRunner):
    """
    Job d'enrichissement des données pour le projet mobilité.

    Cette classe combine plusieurs sources de données :
    - référentiel des gares IDF
    - carte PMR
    - validations réseau ferré
    - établissements critiques
    - état des ascenseurs
    - correspondances et métriques liées aux stations de métro

    Elle calcule également des métriques de proximité (LGF_250m, LGF_500m)
    pour les établissements et intègre le nombre d'ascenseurs par station.
    """

    def __init__(self):
        """
        Initialise tous les chemins d’entrée et de sortie pour le job.

        Attributes:
            ref_gare_path (str): Chemin du fichier GeoParquet des gares.
            carte_pmr_path (str): Chemin du fichier Parquet carte PMR.
            validation_path (str): Chemin du fichier Parquet validations réseau.
            etablissements_path (str): Chemin du fichier GeoParquet établissements.
            ascenseurs_path (str): Chemin du fichier CSV état des ascenseurs.
            corr_nombre_etape_path (str): Chemin du fichier Parquet nombre d’étapes métro.
            corr_path (str): Chemin du fichier Parquet correspondances.
            out_path (str): Chemin du fichier GeoParquet final enrichi.
        """
        self.ref_gare_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/ref_gares.gpq"
        self.carte_pmr_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/carte_pmr.parquet"
        self.validation_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/validation_pourcentage.parquet"
        self.etablissements_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/etablissements.gpq"
        self.ascenseurs_path = "/home/onyxia/work/hackathon_mobilites_2025/data/raw/etat-des-ascenseurs.csv"
        self.corr_nombre_etape_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/metro_connexion_nombre_etape.parquet"
        self.corr_path = "/home/onyxia/work/hackathon_mobilites_2025/data/metro_conexion_qualif.parquet"
        self.out_path = "/home/onyxia/work/hackathon_mobilites_2025/data/enrich/final_table.gpq"

    def process(self):
        """
        Exécute le pipeline complet d'enrichissement des données.

        Étapes principales :
        1. Chargement de toutes les sources (GeoParquet, Parquet, CSV).
        2. Jointures et agrégations pour les correspondances et métriques des stations.
        3. Jointure avec la carte PMR et filtrage des stations pertinentes.
        4. Jointure avec les validations réseau.
        5. Calcul des distances Haversine entre stations et établissements.
        6. Comptage des établissements à moins de 250m et 500m (LGF_250m / LGF_500m).
        7. Comptage du nombre d'ascenseurs par station.
        8. Écriture finale du GeoDataFrame enrichi au format GeoParquet.
        """

        # 1. Chargement des différentes sources de données
        df_ref_gare = LoaderLocal.loader_geoparquet(self.ref_gare_path)
        df_carte_pmr = LoaderLocal.loader_parquet(self.carte_pmr_path)
        df_validation = LoaderLocal.loader_parquet(self.validation_path)
        df_etablissement = LoaderLocal.loader_geoparquet(self.etablissements_path)
        df_ascenseurs = LoaderLocal.loader_csv(self.ascenseurs_path, sep=";")
        df_corr_nombre_etape = LoaderLocal.loader_parquet(self.corr_nombre_etape_path)
        df_corr = LoaderLocal.loader_parquet(self.corr_path)

        # 2. Jointures pour les correspondances métro
        df_corr_nombre_etape_select = df_corr_nombre_etape[["station", "total_nb_etapes"]]

        # Agrégation des métriques moyennes par station
        df_corr_description = df_corr.groupby(["Station", "ID Zone arret ICAR"]).agg(
            moyenne_stairs=('total_stairs', 'mean'),
            moyenne_meters=('total_meters', 'mean'),
            moyenne_asc=('ascendings', 'mean'),
            moyenne_desc=('descendings', 'mean'),
        ).reset_index()

        # Jointure des métriques avec le nombre d’étapes
        df_corr_join = pd.merge(df_corr_description, df_corr_nombre_etape_select,
                                left_on="Station", right_on="station", how="left")

        # Fusion avec le référentiel des gares
        df_ref_gare_corr = pd.merge(df_ref_gare, df_corr_join, how="left",
                                    left_on="id_ref_zda", right_on="ID Zone arret ICAR")

        # 3. Jointure avec la carte PMR
        df_join_carte = pd.merge(df_ref_gare_corr, df_carte_pmr, on='station_clean', how='right')
        df_filter_carte = df_join_carte[
            df_join_carte['ligne'].isna() |
            (df_join_carte['ligne'] == '') |
            (df_join_carte['ligne'] == df_join_carte['res_com'])
        ].copy()

        # 4. Jointure avec les validations
        df_filter_carte['id_ref_zdc'] = df_filter_carte['id_ref_zdc'].astype(str)
        df_validation['id_zdc'] = df_validation['id_zdc'].astype(str)
        df_final = pd.merge(df_filter_carte, df_validation, left_on="id_ref_zdc", right_on="id_zdc", how='left')

        # 5. Préparation des coordonnées des établissements
        df_etab_coords = df_etablissement.copy()
        df_etab_coords['lat'] = df_etab_coords.geometry.y
        df_etab_coords['lng'] = df_etab_coords.geometry.x
        etab_list = list(zip(df_etab_coords['lat'], df_etab_coords['lng']))
        n_etab = len(etab_list)
        print(f"📍 {n_etab} établissements critiques chargés pour calcul de proximité.")

        # Préparation des coordonnées des stations
        df_final = df_final.copy()
        df_final['station_lat'] = df_final.geometry.y
        df_final['station_lng'] = df_final.geometry.x
        df_final['LGF_250m'] = 0
        df_final['LGF_500m'] = 0

        # 6. Calcul des distances Haversine (compte d'établissements à 250m et 500m)
        for idx, row in df_final.iterrows():
            try:
                lat_station = row['station_lat'] if 'station_lat' in row else row['lat']
                lng_station = row['station_lng'] if 'station_lng' in row else row['lng']
            except KeyError as e:
                raise KeyError(f"❌ Colonne de coordonnées manquante dans df_final : {e}. "
                               f"Colonnes disponibles : {list(row.index)}")

            count_250 = 0
            count_500 = 0
            for lat_etab, lng_etab in etab_list:
                dist = self.haversine_m(lat_station, lng_station, lat_etab, lng_etab)
                if dist <= 250:
                    count_250 += 1
                if dist <= 500:
                    count_500 += 1

            df_final.at[idx, 'LGF_250m'] = count_250
            df_final.at[idx, 'LGF_500m'] = count_500
        print("✅ Calcul de LGF_250m / LGF_500m terminé.")

        # 7. Comptage des ascenseurs par station
        df_asc_counts = (
            df_ascenseurs
                .groupby("zdcid")['liftid']
                .nunique()  # compte des ascenseurs uniques
                .reset_index(name='n_lifts')
        )
        df_asc_counts['zdcid'] = df_asc_counts['zdcid'].astype(str)
        df_final['id_ref_zdc'] = df_final['id_ref_zdc'].astype(float).astype('Int64').astype(str)

        # Jointure finale avec les ascenseurs
        df_final_with_ascenseurs = pd.merge(
            df_final,
            df_asc_counts,
            left_on="id_ref_zdc",
            right_on="zdcid",
            how="left"
        )

        # 8. Écriture du GeoDataFrame enrichi final
        WriterLocal.write_geoparquet(df_final_with_ascenseurs, self.out_path)

    def haversine_m(self, lat1, lon1, lat2, lon2):
        """
        Calcule la distance en mètres entre deux points géographiques
        via la formule de Haversine.

        Args:
            lat1, lon1 (float): Coordonnées du premier point.
            lat2, lon2 (float): Coordonnées du second point.

        Returns:
            float: Distance en mètres entre les deux points.
        """
        R = 6371000  # Rayon de la Terre en mètres
        φ1 = radians(lat1)
        φ2 = radians(lat2)
        Δφ = radians(lat2 - lat1)
        Δλ = radians(lon2 - lon1)

        a = sin(Δφ / 2) ** 2 + cos(φ1) * cos(φ2) * sin(Δλ / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
