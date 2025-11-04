from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("usuario", __name__)

@bp.route("/", methods=["POST"])
def crear():
    db = current_app.config["DB"]
    data = request.get_json() or {}
    if not data.get("rut") or not data.get("nombre"):
        return jsonify({"error":"rut y nombre requeridos"}), 400
    try:
        db.usuarios.insert_one(data)
        return jsonify({"msg":"Usuario creado"}), 201
    except:
        return jsonify({"error":"RUT ya existe"}), 400

@bp.route("/", methods=["GET"])
def listar():
    db = current_app.config["DB"]
    return jsonify(list(db.usuarios.find({},{"_id":0}))), 200

@bp.route("/<rut>", methods=["GET"])
def buscar(rut):
    db = current_app.config["DB"]
    u = db.usuarios.find_one({"rut":rut},{"_id":0})
    return jsonify(u) if u else (jsonify({"error":"No encontrado"}), 404)

@bp.route("/<rut>", methods=["DELETE"])
def borrar(rut):
    db = current_app.config["DB"]
    r = db.usuarios.delete_one({"rut":rut})
    return (jsonify({"msg":"Eliminado"}),200) if r.deleted_count else (jsonify({"error":"No existe"}),404)
