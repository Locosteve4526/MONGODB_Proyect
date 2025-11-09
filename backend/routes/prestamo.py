from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("prestamos", __name__)

def col():
    return current_app.config["DB"].prestamos

def usuarios_col():
    return current_app.config["DB"].usuarios

def copias_col():
    return current_app.config["DB"].copias


@bp.route("/", methods=["POST"])
def crear_prestamo():
    data = request.json or {}
    RUT = data.get("RUT")
    ISBN = (data.get("ISBN") or "").strip()
    numero = data.get("numero")
    Fecha_prestamo = (data.get("fecha_prestamo") or "").strip()
    Fecha_devolucion = (data.get("fecha_devolucion") or "").strip()

    if not (RUT and ISBN and numero is not None and Fecha_prestamo and Fecha_devolucion):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # Validación FK
    if not usuarios_col().find_one({"RUT": RUT}):
        return jsonify({"error": f"Usuario no existe: {RUT}"}), 400

    if not copias_col().find_one({"ISBN": ISBN, "numero": numero}):
        return jsonify({"error": f"Copia no existe: ISBN {ISBN} Numero {numero}"}), 400
    
    if col().find_one({"RUT": RUT, "ISBN": ISBN, "numero": numero}):
        return jsonify({"error": f"Ya existe un prestamo con esos datos: RUT {RUT} ISBN {ISBN} Numero {numero}"}), 400

    col().insert_one({
        "RUT": RUT,
        "ISBN": ISBN,
        "numero": numero,
        "fecha_prestamo": Fecha_prestamo,
        "fecha_devolucion": Fecha_devolucion
    })

    return jsonify({"msg": "Préstamo registrado correctamente"}), 201



@bp.route("/", methods=["GET"])
def listar_prestamos():
    docs = list(col().find({}, {"_id": 0}))
    return jsonify(docs), 200



@bp.route("/buscar", methods=["GET"])
def obtener_prestamo():
    RUT = request.args.get("RUT")
    ISBN = request.args.get("ISBN")
    numero = request.args.get("numero", type=int)

    query = {}
    if RUT: query["RUT"] = RUT
    if ISBN: query["ISBN"] = ISBN
    if numero is not None: query["numero"] = numero

    prestamo = col().find_one(query, {"_id": 0})
    if not prestamo:
        return jsonify({"error": "No se encontró el préstamo"}), 404

    return jsonify(prestamo), 200



@bp.route("/<int:RUT>/<string:ISBN>/<int:numero>", methods=["PUT"])
def actualizar_prestamo(RUT, ISBN, numero):
    data = request.json or {}

    if not (RUT and ISBN and numero is not None):
        return jsonify({"error": "Debe enviar RUT, ISBN y numero del préstamo a actualizar"}), 400

    if not col().find_one({"RUT": RUT, "ISBN": ISBN, "numero": numero}):
        return jsonify({"error": "Préstamo no existe"}), 404

    update_fields = {k: v for k, v in data.items() if k not in ["RUT", "ISBN", "numero"]}

    if not update_fields:
        return jsonify({"error": "No hay campos para actualizar"}), 400

    col().update_one({"RUT": RUT, "ISBN": ISBN, "numero": numero}, {"$set": update_fields})

    return jsonify({"msg": "Préstamo actualizado correctamente"}), 200



@bp.route("/<int:RUT>/<string:ISBN>/<int:numero>", methods=["DELETE"])
def eliminar_prestamo(RUT, ISBN, numero):
    if not (RUT and ISBN and numero is not None):
        return jsonify({"error": "Debe enviar RUT, ISBN y numero del préstamo a eliminar"}), 400

    res = col().delete_one({"RUT": RUT, "ISBN": ISBN, "numero": numero})

    if res.deleted_count == 0:
        return jsonify({"error": "Préstamo no encontrado"}), 404

    return jsonify({"msg": "Préstamo eliminado correctamente"}), 200