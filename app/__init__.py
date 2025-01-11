from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import main_blueprint  # Importa el Blueprint desde routes.py

# Cargar variables de entorno
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuración basada en variables de entorno
    app.config['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
    if not app.config['OPENAI_API_KEY']:
        raise ValueError("La clave de API de OpenAI (OPENAI_API_KEY) no está configurada.")

    # Registrar el Blueprint
    app.register_blueprint(main_blueprint)

    return app
