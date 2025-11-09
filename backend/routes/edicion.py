from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("ediciones", __name__)

def col():
    return current_app.config["DB"].ediciones

def libros_col():
    return current_app.config["DB"].libros

@bp.route("/", methods=["POST"])
def crear_edicion():
    data = request.json or {}
    ISBN = (data.get("ISBN") or "").strip()
    titulo = (data.get("titulo") or "").strip()
    anio = data.get("anio")
    idioma = (data.get("idioma") or "").strip()
    if not ISBN or not titulo or anio is None or not idioma:
        return jsonify({"error": "Faltan campos: ISBN, titulo, anio, idioma"}), 400
    # verificar que el libro exista
    if not libros_col().find_one({"titulo": titulo}):
        return jsonify({"error": f"Libro no existe: {titulo}"}), 400
    if col().find_one({"ISBN": ISBN}):
        return jsonify({"error": "Edicion ya existe"}), 400
    col().insert_one({"ISBN": ISBN, "titulo": titulo, "anio": anio, "idioma": idioma})
    return jsonify({"msg": "Edicion creada", "ISBN": ISBN}), 201

@bp.route("/", methods=["GET"])
def listar_ediciones():
    docs = list(col().find({}, {"_id": 0}))
    return jsonify(docs), 200

@bp.route("/<string:ISBN>", methods=["GET"])
def obtener_edicion(ISBN):
    doc = col().find_one({"ISBN": ISBN}, {"_id": 0})
    if not doc:
        return jsonify({"error": "Edicion no encontrada"}), 404
    return jsonify(doc), 200

@bp.route("/<string:ISBN>", methods=["PUT"])
def actualizar_edicion(ISBN):
    data = request.json or {}
    if "titulo" in data:
        if not libros_col().find_one({"titulo": data["titulo"]}):
            return jsonify({"error": f"Libro no existe: {data['titulo']}"}), 400
    res = col().update_one({"ISBN": ISBN}, {"$set": data})
    if res.matched_count == 0:
        return jsonify({"error": "Edicion no encontrada"}), 404
    return jsonify({"msg": "Edicion actualizada"}), 200

@bp.route("/<string:ISBN>", methods=["DELETE"])
def borrar_edicion(ISBN):
    res = col().delete_one({"ISBN": ISBN})
    if res.deleted_count == 0:
        return jsonify({"error": "Edicion no encontrada"}), 404
    return jsonify({"msg": "Edicion eliminada"}), 200