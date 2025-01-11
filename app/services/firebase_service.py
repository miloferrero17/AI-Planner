import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase Admin SDK
def initialize_firebase():
    # Ruta al archivo de credenciales del servicio (Service Account Key)
    cred = credentials.Certificate("credentials/service-account.json")
    firebase_admin.initialize_app(cred)

# Inicializar Firestore
def get_firestore_client():
    # Asegúrate de que Firebase ya está inicializado antes de llamar a esta función
    return firestore.client()


# Inicializar Firebase automáticamente al importar este archivo
try:
    initialize_firebase()
    db = get_firestore_client()
    print("Firebase y Firestore inicializados correctamente.")
except Exception as e:
    print(f"Error al inicializar Firebase: {e}")
