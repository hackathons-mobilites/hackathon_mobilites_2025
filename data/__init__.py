import os
from posixpath import join

DATA_PATH = os.path.dirname(__file__)
FILTERED_DATA_PATH = os.path.join(DATA_PATH, "filtered")

PATH_PARKING_VELO = join(DATA_PATH, "parking_velo.parquet")
