from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("libros", __name__)

def col():
    return current_app.config["DB"].libros

def autores_col():
    return current_app.config["DB"].autores

@bp.route("/", methods=["POST"])
def crear_libro():
    data = request.json or {}
    titulo = (data.get("titulo") or "").strip()
    autores = data.get("autores", [])
    if not titulo:
        return jsonify({"error": "Falta titulo"}), 400
    if not isinstance(autores, list) or len(autores) == 0:
        return jsonify({"error": "Falta autores (lista de nombres)"}), 400
    # verificar existencia de autores por nombre
    for a in autores:
        if not autores_col().find_one({"nombre": a}):
            return jsonify({"error": f"Autor no existe: {a}"}), 400
    if col().find_one({"titulo": titulo}):
        return jsonify({"error": "Libro ya existe"}), 400
    col().insert_one({"titulo": titulo, "autores": autores})
    return jsonify({"msg": "Libro creado", "titulo": titulo}), 201

@bp.route("/", methods=["GET"])
def listar_libros():
    docs = list(col().find({}, {"_id": 0}))
    return jsonify(docs), 200

@bp.route("/<path:titulo>", methods=["GET"])
def obtener_libro(titulo):
    doc = col().find_one({"titulo": titulo}, {"_id": 0})
    if not doc:
        return jsonify({"error": "Libro no encontrado"}), 404
    return jsonify(doc), 200

@bp.route("/<path:titulo>", methods=["PUT"])
def actualizar_libro(titulo):
    data = request.json or {}
    if "autores" in data:
        for a in data["autores"]:
            if not autores_col().find_one({"nombre": a}):
                return jsonify({"error": f"Autor no existe: {a}"}), 400
    res = col().update_one({"titulo": titulo}, {"$set": data})
    if res.matched_count == 0:
        return jsonify({"error": "Libro no encontrado"}), 404
    return jsonify({"msg": "Libro actualizado"}), 200

@bp.route("/<path:titulo>", methods=["DELETE"])
def borrar_libro(titulo):
    res = col().delete_one({"titulo": titulo})
    if res.deleted_count == 0:
        return jsonify({"error": "Libro no encontrado"}), 404
    return jsonify({"msg": "Libro eliminado"}), 200
