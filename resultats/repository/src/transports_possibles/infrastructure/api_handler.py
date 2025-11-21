import pandas as pd
import boto3

from src.transports_possibles.domain.ports.source_handler import SourceHandler
from config.var_env import (
    ACCESS_KEY,
    SECRET_KEY,
    SESSION_TOKEN,
    REGION,
    ENDPOINT_URL,
    BUCKET,
)

FILE_KEY_S3 = "/datasets-diffusion/2025/12_Donnees_transilien_SNCF/Capacité emport vélos.csv"


class ApiHandler(SourceHandler):
    def get_transports_possibles_data(self) -> pd.DataFrame:
        s3 = boto3.client(
            "s3",
            endpoint_url="https://" + ENDPOINT_URL,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            aws_session_token=SESSION_TOKEN,
            region_name=REGION,
        )
        response = s3.get_object(Bucket=BUCKET, Key=FILE_KEY_S3)
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status == 200:
            return pd.read_csv(response.get("Body"), sep=";")
        else:
            raise Exception(f"Failed to fetch data from S3. Status code: {status}")
