from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.config.Config")

    # Registrar rutas
    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
