from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("autores", __name__)


def col():
    return current_app.config["DB"].autores

@bp.route("/", methods=["POST"])
def crear_autor():
    data = request.json or {}
    nombre = (data.get("nombre") or "").strip()
    if not nombre:
        return jsonify({"error": "Falta nombre"}), 400
    if col().find_one({"nombre": nombre}):
        return jsonify({"error": "Autor ya existe"}), 400
    col().insert_one({"nombre": nombre})
    return jsonify({"msg": "Autor creado", "nombre": nombre}), 201

@bp.route("/", methods=["GET"])
def listar_autores():
    docs = list(col().find({}, {"_id": 0}))
    return jsonify(docs), 200

@bp.route("/<string:nombre>", methods=["GET"])
def obtener_autor(nombre):
    doc = col().find_one({"nombre": nombre}, {"_id": 0})
    if not doc:
        return jsonify({"error": "Autor no encontrado"}), 404
    return jsonify(doc), 200

@bp.route("/<string:nombre>", methods=["PUT"])
def actualizar_autor(nombre):
    data = request.json or {}
    nuevo_nombre = data.get("nombre")
    if nuevo_nombre and nuevo_nombre != nombre:
        if col().find_one({"nombre": nuevo_nombre}):
            return jsonify({"error": "Nuevo nombre ya existe"}), 400
    res = col().update_one({"nombre": nombre}, {"$set": data})
    if res.matched_count == 0:
        return jsonify({"error": "Autor no encontrado"}), 404
    return jsonify({"msg": "Autor actualizado"}), 200

@bp.route("/<string:nombre>", methods=["DELETE"])
def borrar_autor(nombre):
    res = col().delete_one({"nombre": nombre})
    if res.deleted_count == 0:
        return jsonify({"error": "Autor no encontrado"}), 404
    return jsonify({"msg": "Autor eliminado"}), 200
