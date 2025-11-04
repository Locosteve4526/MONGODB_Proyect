from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("edicion", __name__)

@bp.route("/", methods=["POST"])
def crear():
    db = current_app.config["DB"]
    d = request.get_json() or {}

    if not all([d.get("ISBN"), d.get("libro"), d.get("año"), d.get("idioma")]):
        return jsonify({"error":"campos requeridos: ISBN, libro, año, idioma"}), 400

    if db.ediciones.find_one({"ISBN": d["ISBN"]}):
        return jsonify({"error":"ISBN ya existe"}), 400

    if not db.libros.find_one({"titulo": d["libro"]}):
        return jsonify({"error":"El libro no existe"}), 400

    db.ediciones.insert_one(d)
    return jsonify({"msg":"Edición creada"}), 201


@bp.route("/", methods=["GET"])
def listar():
    db = current_app.config["DB"]
    return jsonify(list(db.ediciones.find({},{"_id":0}))), 200
