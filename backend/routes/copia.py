from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("copias", __name__)

def col():
    return current_app.config["DB"].copias

def col():
    return current_app.config["DB"].copias

def ediciones_col():
    return current_app.config["DB"].ediciones

@bp.route("/", methods=["POST"])
def crear_copia():
    data = request.json or {}
    ISBN = (data.get("ISBN") or "").strip()
    numero = data.get("numero")
    if not ISBN or numero is None:
        return jsonify({"error": "Faltan ISBN o numero"}), 400
    # verificar existencia de edicion
    if not ediciones_col().find_one({"ISBN": ISBN}):
        return jsonify({"error": f"Edicion no existe: {ISBN}"}), 400
    # intentar insertar (índice único compuesto evita duplicados)
    try:
        col().insert_one({"ISBN": ISBN, "numero": int(numero)})
    except Exception as e:
        return jsonify({"error": "No se pudo insertar copia (posible duplicado)", "detail": str(e)}), 400
    return jsonify({"msg": "Copia creada", "ISBN": ISBN, "numero": numero}), 201

@bp.route("/", methods=["GET"])
def listar_copias():
    docs = list(col().find({}, {"_id": 0}))
    return jsonify(docs), 200

@bp.route("/<string:ISBN>/<int:numero>", methods=["GET"])
def obtener_copia(ISBN, numero):
    doc = col().find_one({"ISBN": ISBN, "numero": numero}, {"_id": 0})
    if not doc:
        return jsonify({"error": "Copia no encontrada"}), 404
    return jsonify(doc), 200

@bp.route("/<string:ISBN>/<int:numero>", methods=["PUT"])
def actualizar_copia(ISBN, numero):
    data = request.json or {}
    if "numero" in data and int(data["numero"]) != numero:
        # verificar no choque de clave compuesta
        if col().find_one({"ISBN": ISBN, "numero": int(data["numero"])}):
            return jsonify({"error": "Ya existe otra copia con ese numero para esta edicion"}), 400
    res = col().update_one({"ISBN": ISBN, "numero": numero}, {"$set": data})
    if res.matched_count == 0:
        return jsonify({"error": "Copia no encontrada"}), 404
    return jsonify({"msg": "Copia actualizada"}), 200

@bp.route("/<string:ISBN>/<int:numero>", methods=["DELETE"])
def borrar_copia(ISBN, numero):
    res = col().delete_one({"ISBN": ISBN, "numero": numero})
    if res.deleted_count == 0:
        return jsonify({"error": "Copia no encontrada"}), 404
    return jsonify({"msg": "Copia eliminada"}), 200
