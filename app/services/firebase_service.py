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

# **Funciones CRUD para Firestore**
def add_user(collection_name, document_id, data):
    """
    Crea o actualiza un documento en la colección especificada.

    Args:
        collection_name (str): Nombre de la colección.
        document_id (str): ID único del documento.
        data (dict): Datos a guardar en el documento.
    """
    try:
        create_or_update_document_with_merge(collection_name, document_id, data)
    except Exception as e:
        print(f"Error al agregar el usuario: {e}")

# Crear o actualizar un documento sin sobrescribir datos existentes
def create_or_update_document(collection_name, document_id, data):
    try:
        doc_ref = db.collection(collection_name).document(document_id)
        
        # Obtener los datos actuales del documento
        doc = doc_ref.get()
        if doc.exists:
            # Mezclar los datos existentes con los nuevos
            existing_data = doc.to_dict()
            merged_data = {**existing_data, **data}  # Priorizará los nuevos valores en caso de conflicto
            doc_ref.set(merged_data)
            #print(f"Documento {document_id} actualizado correctamente con mezcla de datos en la colección {collection_name}.")
        else:
            # Si no existe, crearlo con los nuevos datos
            doc_ref.set(data)
            #print(f"Documento {document_id} creado correctamente en la colección {collection_name}.")
    except Exception as e:
        print(f"Error al crear/actualizar el documento {document_id}: {e}")

# Leer un documento
def read_document(collection_name, document_id):
    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            print(f"Documento {document_id} leído correctamente: {doc.to_dict()}")
            return doc.to_dict()
        else:
            print(f"El documento {document_id} no existe en la colección {collection_name}.")
            return None
    except Exception as e:
        print(f"Error al leer el documento {document_id}: {e}")

# Actualizar campos de un documento
def update_document(collection_name, document_id, data):
    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.update(data)
        print(f"Documento {document_id} actualizado correctamente en la colección {collection_name}.")
    except Exception as e:
        print(f"Error al actualizar el documento {document_id}: {e}")

# Eliminar un documento
def delete_document(collection_name, document_id):
    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.delete()
        print(f"Documento {document_id} eliminado correctamente de la colección {collection_name}.")
    except Exception as e:
        print(f"Error al eliminar el documento {document_id}: {e}")
