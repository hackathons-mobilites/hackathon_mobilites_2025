from utils.job_runner import JobRunner
from utils.loader_local import LoaderLocal
from utils.writer_local import WriterLocal
import pandas as pd
from math import radians, sin, cos, sqrt, atan2


class EnrichJob(JobRunner):
    def __init__(self):
        self.ref_gare_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/ref_gares.gpq"
        self.carte_pmr_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/carte_pmr.parquet"
        self.validation_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/validation_pourcentage.parquet"
        self.etablissements_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/etablissements.gpq"
        self.out_path = "/home/onyxia/work/hackathon_mobilites_2025/data/enrich/final_table.gpq"

    def process(self):
        df_ref_gare = LoaderLocal.loader_geoparquet(self.ref_gare_path)
        df_carte_pmr = LoaderLocal.loader_parquet(self.carte_pmr_path)
        df_validation = LoaderLocal.loader_parquet(self.validation_path)
        df_etablissement = LoaderLocal.loader_geoparquet(self.etablissements_path)

        # Jointure avec la carte PMR
        df_join_carte = pd.merge(df_ref_gare, df_carte_pmr, on='station_clean', how='right')
        df_filter_carte = df_join_carte[
            df_join_carte['ligne'].isna() |
            (df_join_carte['ligne'] == '') |
            (df_join_carte['ligne'] == df_join_carte['res_com'])
        ].copy()
        # Jointure avec les validations
        df_filter_carte['id_ref_zdc'] = df_filter_carte['id_ref_zdc'].astype(str)
        df_validation['id_zdc'] = df_validation['id_zdc'].astype(str)
        df_final = pd.merge(df_filter_carte, df_validation, left_on="id_ref_zdc", right_on="id_zdc", how='left')

        # Calcul des distances
        df_etab_coords = df_etablissement.copy()
        df_etab_coords['lat'] = df_etab_coords.geometry.y
        df_etab_coords['lng'] = df_etab_coords.geometry.x

        etab_list = list(zip(df_etab_coords['lat'], df_etab_coords['lng']))
        n_etab = len(etab_list)
        print(f"📍 {n_etab} établissements critiques chargés pour calcul de proximité.")

        def haversine_m(lat1, lon1, lat2, lon2):
            R = 6371000  # Rayon de la Terre en mètres
            φ1 = radians(lat1)
            φ2 = radians(lat2)
            Δφ = radians(lat2 - lat1)
            Δλ = radians(lon2 - lon1)

            a = sin(Δφ / 2) ** 2 + cos(φ1) * cos(φ2) * sin(Δλ / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        df_final = df_final.copy()
        df_final['station_lat'] = df_final.geometry.y
        df_final['station_lng'] = df_final.geometry.x

        df_final['LGF_250m'] = 0
        df_final['LGF_500m'] = 0

        # 🔹 Itération (ligne par ligne)
        print("🔍 Calcul des distances (Haversine) — peut être lent si grand volume...")
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
                dist = haversine_m(lat_station, lng_station, lat_etab, lng_etab)
                if dist <= 250:
                    count_250 += 1
                if dist <= 500:
                    count_500 += 1

            df_final.at[idx, 'LGF_250m'] = count_250
            df_final.at[idx, 'LGF_500m'] = count_500

        print("✅ Calcul de LGF_250m / LGF_500m terminé.")

        # Ecriture en GeoParquet
        WriterLocal.write_geoparquet(df_final, self.out_path)
