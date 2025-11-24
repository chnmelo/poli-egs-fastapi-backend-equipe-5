# key_admin.py
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

# Load environment variables from .env file
load_dotenv()

def initialize_firebase():
    private_key = os.getenv("FIREBASE_PRIVATE_KEY")
    if private_key:
        # Isso converte os caracteres literais "\n" em quebras de linha reais
        private_key = private_key.replace('\\n', '\n')
    if not private_key:
        raise ValueError("A variável de ambiente FIREBASE_PRIVATE_KEY não está definida. Verifique seu arquivo .env.")

    # Construct Firebase credentials from environment variables
    firebase_creds = {
        "type": os.getenv("FIREBASE_TYPE"),
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": private_key.replace("\\n", "\n"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    }

    # Initialize Firebase Admin SDK if not already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'ecomp-observatorio.appspot.com'  # nome do bucket do Firebase
        })

# Initialize Firebase on import
initialize_firebase()
