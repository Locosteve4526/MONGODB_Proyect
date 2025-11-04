from flask import Blueprint, current_app, jsonify, request, abort

bp = Blueprint("copia", __name__)

# Colección: copias
# Documento:
# { "ISBN": "string", "numero": int }

@bp.route("/", methods=["POST"])
def crear_copia():
    db = current_app.config["DB"]
    data = request.get_json() or {}

    ISBN = data.get("ISBN")
    numero = data.get("numero")

    if not ISBN or numero is None:
        return jsonify({"error": "Se requieren ISBN y numero"}), 400
    
    try:
        numero = int(numero)
    except:
        return jsonify({"error": "numero debe ser entero"}), 400

    if db.ediciones.find_one({"ISBN": ISBN}) is None:
        return jsonify({"error": "No existe una edición con ese ISBN"}), 400

    if db.copias.find_one({"ISBN": ISBN, "numero": numero}):
        return jsonify({"error": "La copia ya existe"}), 400
    
    db.copias.insert_one({"ISBN": ISBN, "numero": numero})
    return jsonify({"msg": "Copia creada"}), 201


@bp.route("/", methods=["GET"])
def listar_copias():
    db = current_app.config["DB"]
    docs = list(db.copias.find({}, {"_id":0}))
    return jsonify(docs), 200


@bp.route("/<isbn>/<int:numero>", methods=["GET"])
def obtener_copia(isbn, numero):
    db = current_app.config["DB"]
    copia = db.copias.find_one({"ISBN": isbn, "numero": numero}, {"_id": 0})

    if not copia:
        return jsonify({"error": "Copia no encontrada"}), 404

    return jsonify(copia), 200


@bp.route("/<isbn>/<int:numero>", methods=["DELETE"])
def eliminar_copia(isbn, numero):
    db = current_app.config["DB"]
    res = db.copias.delete_one({"ISBN": isbn, "numero": numero})

    if res.deleted_count == 0:
        return jsonify({"error": "Copia no encontrada"}), 404
    
    return jsonify({"msg": "Copia eliminada"}), 200