from flask import Flask, jsonify
from flask_cors import CORS
from config import MONGO_URI, DB_NAME
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Inyecta db para usar en routes
    app.config["DB"] = db

    # registrar blueprints
    from routes.autor import bp as autor_bp
    from routes.libro import bp as libro_bp
    from routes.edicion import bp as edicion_bp
    from routes.copia import bp as copia_bp
    from routes.usuario import bp as usuario_bp
    from routes.prestamo import bp as prestamo_bp
    from routes.consultas import bp as consultas_bp

    app.register_blueprint(autor_bp, url_prefix="/autores")
    app.register_blueprint(libro_bp, url_prefix="/libros")
    app.register_blueprint(edicion_bp, url_prefix="/ediciones")
    app.register_blueprint(copia_bp, url_prefix="/copias")
    app.register_blueprint(usuario_bp, url_prefix="/usuarios")
    app.register_blueprint(prestamo_bp, url_prefix="/prestamos")
    app.register_blueprint(consultas_bp, url_prefix="/consultas")

    @app.route("/")
    def home():
        return jsonify({"msg": "API Biblioteca en Flask - funcionando"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
