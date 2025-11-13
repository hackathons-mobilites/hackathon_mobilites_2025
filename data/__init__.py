import os
from posixpath import join

DATA_PATH = os.path.dirname(__file__)

PATH_PARKING_VELO = join(DATA_PATH, "parking_velo.parquet")
