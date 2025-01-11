from app.services.firebase_service import db

def test_firestore():
    try:
        # Crea un documento de prueba
        doc_ref = db.collection("test_collection").document("test_document")
        doc_ref.set({"field1": "value1", "field2": "value2"})
        print("Documento creado correctamente en Firestore.")

        # Lee el documento de prueba
        doc = doc_ref.get()
        if doc.exists:
            print("Contenido del documento:", doc.to_dict())
        else:
            print("El documento no existe.")

        # Actualiza el documento de prueba
        doc_ref.update({"field2": "updated_value"})
        print("Documento actualizado correctamente.")

        # Elimina el documento de prueba
        doc_ref.delete()
        print("Documento eliminado correctamente.")
    except Exception as e:
        print(f"Error durante la prueba de Firestore: {e}")

# Ejecuta la prueba
test_firestore()
