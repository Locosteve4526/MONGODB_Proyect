from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("usuarios", __name__)

def col():
    return current_app.config["DB"].usuarios

@bp.route("/", methods=["POST"])
def crear_usuario():
    data = request.json or {}
    RUT = (data.get("RUT") or "").strip()
    nombre = (data.get("nombre") or "").strip()
    if not RUT or not nombre:
        return jsonify({"error": "Faltan RUT o nombre"}), 400
    if col().find_one({"RUT": RUT}):
        return jsonify({"error": "Usuario ya existe"}), 400
    col().insert_one({"RUT": RUT, "nombre": nombre})
    return jsonify({"msg": "Usuario creado", "RUT": RUT}), 201

@bp.route("/", methods=["GET"])
def listar_usuarios():
    docs = list(col().find({}, {"_id": 0}))
    return jsonify(docs), 200

@bp.route("/<string:RUT>", methods=["GET"])
def obtener_usuario(RUT):
    doc = col().find_one({"RUT": RUT}, {"_id": 0})
    if not doc:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(doc), 200

@bp.route("/<string:RUT>", methods=["PUT"])
def actualizar_usuario(RUT):
    data = request.json or {}
    if "RUT" in data and data["RUT"] != RUT:
        if col().find_one({"RUT": data["RUT"]}):
            return jsonify({"error": "Nuevo RUT ya existe"}), 400
    res = col().update_one({"RUT": RUT}, {"$set": data})
    if res.matched_count == 0:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"msg": "Usuario actualizado"}), 200

@bp.route("/<string:RUT>", methods=["DELETE"])
def borrar_usuario(RUT):
    res = col().delete_one({"RUT": RUT})
    if res.deleted_count == 0:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"msg": "Usuario eliminado"}), 200
