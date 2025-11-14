from extract.job.carte_pmr_job import CartePmrJob
from extract.job.ref_gare_idf_job import RefGareIdfJob
from extract.job.etablissement_job import EtablissementJob
from extract.job.validation_job import ValidationJob
from enrich.job.enrich_job import EnrichJob
from enrich.job.classification_stations_job import ClassificationStationsJob

# Job d'ingestion et de mise en qualité des sources de données
CartePmrJob().process()
RefGareIdfJob().process()
EtablissementJob().process()
ValidationJob().process()

# Job d'enrichissement de la données (Jointure + calcul des points GPS a coté)
EnrichJob().process()
ClassificationStationsJob().process()
