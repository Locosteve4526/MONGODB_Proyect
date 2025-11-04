from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("libro", __name__)

@bp.route("/", methods=["POST"])
def crear():
    db = current_app.config["DB"]
    d = request.get_json() or {}

    if not d.get("titulo") or not d.get("autores"):
        return jsonify({"error":"titulo y autores requeridos"}), 400

    db.libros.insert_one({"titulo": d["titulo"], "autores": d["autores"]})
    return jsonify({"msg":"Libro creado"}), 201

@bp.route("/", methods=["GET"])
def listar():
    db = current_app.config["DB"]
    return jsonify(list(db.libros.find({},{"_id":0}))), 200
