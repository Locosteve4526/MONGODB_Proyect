from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("autor", __name__)

@bp.route("/", methods=["POST"])
def crear():
    db = current_app.config["DB"]
    data = request.get_json() or {}
    if not data.get("nombre"):
        return jsonify({"error":"nombre requerido"}), 400
    db.autores.insert_one(data)
    return jsonify({"msg":"Autor creado"}), 201

@bp.route("/", methods=["GET"])
def listar():
    db = current_app.config["DB"]
    return jsonify(list(db.autores.find({},{"_id":0}))), 200
