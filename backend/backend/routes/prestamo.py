from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("prestamos", __name__)

def col():
    return current_app.config["DB"].prestamos

def copias_col():
    return current_app.config["DB"].copias

@bp.route("/", methods=["POST"])
def crear_prestamo():
    data = request.json
    # data debe contener: usuario_id (string), copia_id (string), fecha_prestamo, fecha_devolucion_estimada
    copia = copias_col().find_one({"_id": ObjectId(data["copia_id"])})
    if not copia:
        return jsonify({"error": "Copia no existe"}), 404
    if copia.get("estado") == "Prestado":
        return jsonify({"error": "Copia ya prestada"}), 400

    # Insertar préstamo
    res = col().insert_one({
        "usuario_id": ObjectId(data["usuario_id"]),
        "copia_id": ObjectId(data["copia_id"]),
        "fecha_prestamo": data["fecha_prestamo"],
        "fecha_devolucion_estimada": data["fecha_devolucion_estimada"],
        "fecha_devolucion_real": None,
        "estado": "Prestado"
    })
    # actualizar copia
    copias_col().update_one({"_id": ObjectId(data["copia_id"])}, {"$set": {"estado": "Prestado"}})
    return jsonify({"_id": str(res.inserted_id)}), 201

@bp.route("/<id>/devolver", methods=["POST"])
def devolver_prestamo(id):
    data = request.json  # { "fecha_devolucion_real": "YYYY-MM-DD" }
    prest = col().find_one({"_id": ObjectId(id)})
    if not prest:
        return jsonify({"error": "Préstamo no encontrado"}), 404
    # actualizar préstamo
    col().update_one({"_id": ObjectId(id)}, {"$set": {"fecha_devolucion_real": data["fecha_devolucion_real"], "estado": "Devuelto"}})
    # actualizar copia
    copias_col().update_one({"_id": prest["copia_id"]}, {"$set": {"estado": "Disponible"}})
    return jsonify({"msg": "Devolución registrada"}), 200
