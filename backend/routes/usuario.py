from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("usuarios", __name__)

def col():
    return current_app.config["DB"].usuarios

@bp.route("/", methods=["POST"])
def crear_usuario():
    data = request.json
    # Validar campos mínimos
    required = ["nombre", "apellido", "documento"]
    for f in required:
        if f not in data:
            return jsonify({"error": f"Falta {f}"}), 400
    res = col().insert_one(data)
    return jsonify({"_id": str(res.inserted_id)}), 201

@bp.route("/", methods=["GET"])
def listar_usuarios():
    docs = list(col().find())
    for d in docs:
        d["_id"] = str(d["_id"])
    return jsonify(docs), 200

@bp.route("/<id>", methods=["GET"])
def obtener_usuario(id):
    doc = col().find_one({"_id": ObjectId(id)})
    if not doc:
        return jsonify({"error": "No encontrado"}), 404
    doc["_id"] = str(doc["_id"])
    return jsonify(doc), 200

@bp.route("/<id>", methods=["PUT"])
def actualizar_usuario(id):
    data = request.json
    res = col().update_one({"_id": ObjectId(id)}, {"$set": data})
    if res.matched_count == 0:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"modified": res.modified_count}), 200

@bp.route("/<id>", methods=["DELETE"])
def borrar_usuario(id):
    res = col().delete_one({"_id": ObjectId(id)})
    if res.deleted_count == 0:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"deleted": res.deleted_count}), 200
