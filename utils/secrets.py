import os
from dotenv import load_dotenv
from google.cloud import secretmanager

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
VERSION = os.getenv("GOOGLE_CLOUD_SECRET_VERSION")

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{VERSION}"
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode("UTF-8")