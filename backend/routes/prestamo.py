from flask import Blueprint, current_app, jsonify, request
from datetime import datetime

bp = Blueprint("prestamo", __name__)

# Documento:
# { "rut": "...", "ISBN": "...", "numero": int, "fecha_prestamo": "...", "fecha_devolucion": None }

@bp.route("/", methods=["POST"])
def crear_prestamo():
    db = current_app.config["DB"]
    data = request.get_json() or {}

    rut = data.get("rut")
    ISBN = data.get("ISBN")
    numero = data.get("numero")

    if not (rut and ISBN and numero is not None):
        return jsonify({"error":"rut, ISBN y numero requeridos"}), 400
    
    try:
        numero = int(numero)
    except:
        return jsonify({"error":"numero debe ser entero"}), 400

    if not db.usuarios.find_one({"rut": rut}):
        return jsonify({"error":"Usuario no existe"}), 400

    if not db.copias.find_one({"ISBN": ISBN, "numero": numero}):
        return jsonify({"error":"Copia no existe"}), 400

    prestado = db.prestamos.find_one({"ISBN": ISBN, "numero": numero, "fecha_devolucion": None})
    if prestado:
        return jsonify({"error":"La copia ya está prestada"}), 400

    fecha = datetime.utcnow().isoformat()
    doc = {"rut": rut, "ISBN": ISBN, "numero": numero, "fecha_prestamo": fecha, "fecha_devolucion": None}

    db.prestamos.insert_one(doc)
    return jsonify({"msg":"Prestamo registrado"}), 201


@bp.route("/devolver", methods=["POST"])
def devolver():
    db = current_app.config["DB"]
    data = request.get_json() or {}

    rut = data.get("rut")
    ISBN = data.get("ISBN")
    numero = data.get("numero")

    if not (rut and ISBN and numero is not None):
        return jsonify({"error":"rut, ISBN y numero requeridos"}), 400

    p = db.prestamos.find_one({"rut": rut, "ISBN": ISBN, "numero": numero, "fecha_devolucion": None})
    if not p:
        return jsonify({"error":"No existe préstamo activo"}), 404

    fecha = datetime.utcnow().isoformat()
    db.prestamos.update_one({"_id": p["_id"]}, {"$set": {"fecha_devolucion": fecha}})
    
    return jsonify({"msg": "Devuelto correctamente"}), 200


@bp.route("/", methods=["GET"])
def listar():
    db = current_app.config["DB"]
    return jsonify(list(db.prestamos.find({},{"_id":0}))), 200
