import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_PRIM = os.getenv("API_KEY_PRIM", "default")
BASE_URL_PRIM = os.getenv("BASE_URL_PRIM", "default")
PATH_CALCULATEUR_IDFM = os.getenv("PATH_CALCULATEUR_IDFM", "default")
PATH_GEOVELO = os.getenv("PATH_GEOVELO", "default")


ACCESS_KEY = os.getenv("ACCESS_KEY", "default")
SECRET_KEY = os.getenv("SECRET_KEY", "default")
SESSION_TOKEN = os.getenv("SESSION_TOKEN", "default")
REGION = os.getenv("REGION", "default")
ENDPOINT_URL = os.getenv("ENDPOINT_URL", "default")

BUCKET = os.getenv("BUCKET", "default")

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY", "default")

METEO_API_KEY = os.getenv("METEO_API_KEY", "default")