from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("ediciones", __name__)

def col():
    return current_app.config["DB"].ediciones

@bp.route("/", methods=["POST"])
def crear_edicion():
    data = request.json
    if "libro_id" not in data:
        return jsonify({"error": "Falta libro_id"}), 400
    data["libro_id"] = ObjectId(data["libro_id"])
    res = col().insert_one(data)
    return jsonify({"_id": str(res.inserted_id)}), 201

@bp.route("/", methods=["GET"])
def listar_ediciones():
    docs = list(col().find())
    for d in docs:
        d["_id"] = str(d["_id"])
        d["libro_id"] = str(d["libro_id"])
    return jsonify(docs), 200

@bp.route("/<id>", methods=["GET"])
def obtener_edicion(id):
    doc = col().find_one({"_id": ObjectId(id)})
    if not doc:
        return jsonify({"error": "No encontrado"}), 404
    doc["_id"] = str(doc["_id"])
    doc["libro_id"] = str(doc["libro_id"])
    return jsonify(doc), 200

@bp.route("/<id>", methods=["PUT"])
def actualizar_edicion(id):
    data = request.json
    if "libro_id" in data:
        data["libro_id"] = ObjectId(data["libro_id"])
    res = col().update_one({"_id": ObjectId(id)}, {"$set": data})
    if res.matched_count == 0:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"modified": res.modified_count}), 200

@bp.route("/<id>", methods=["DELETE"])
def borrar_edicion(id):
    res = col().delete_one({"_id": ObjectId(id)})
    if res.deleted_count == 0:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"deleted": res.deleted_count}), 200
