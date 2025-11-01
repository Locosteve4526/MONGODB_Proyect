from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("copias", __name__)

def col():
    return current_app.config["DB"].copias

@bp.route("/", methods=["POST"])
def crear_copia():
    data = request.json
    if "edicion_id" not in data:
        return jsonify({"error": "Falta edicion_id"}), 400
    data["edicion_id"] = ObjectId(data["edicion_id"])
    if "estado" not in data:
        data["estado"] = "Disponible"
    res = col().insert_one(data)
    return jsonify({"_id": str(res.inserted_id)}), 201

@bp.route("/", methods=["GET"])
def listar_copias():
    docs = list(col().find())
    for d in docs:
        d["_id"] = str(d["_id"])
        d["edicion_id"] = str(d["edicion_id"])
    return jsonify(docs), 200

@bp.route("/<id>", methods=["GET"])
def obtener_copia(id):
    doc = col().find_one({"_id": ObjectId(id)})
    if not doc:
        return jsonify({"error": "No encontrado"}), 404
    doc["_id"] = str(doc["_id"])
    doc["edicion_id"] = str(doc["edicion_id"])
    return jsonify(doc), 200

@bp.route("/<id>", methods=["PUT"])
def actualizar_copia(id):
    data = request.json
    if "edicion_id" in data:
        data["edicion_id"] = ObjectId(data["edicion_id"])
    res = col().update_one({"_id": ObjectId(id)}, {"$set": data})
    if res.matched_count == 0:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"modified": res.modified_count}), 200

@bp.route("/<id>", methods=["DELETE"])
def borrar_copia(id):
    res = col().delete_one({"_id": ObjectId(id)})
    if res.deleted_count == 0:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"deleted": res.deleted_count}), 200
