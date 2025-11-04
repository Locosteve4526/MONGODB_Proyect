from flask import Blueprint, current_app, jsonify, request
from bson.objectid import ObjectId

bp = Blueprint("consultas", __name__)

@bp.route("/copias_con_detalle", methods=["GET"])
def copias_con_detalle():
    db = current_app.config["DB"]
    pipeline = [
        # unir copia -> edicion
        {"$lookup": {
            "from": "ediciones",
            "localField": "edicion_id",
            "foreignField": "_id",
            "as": "edicion"
        }},
        {"$unwind": {"path": "$edicion", "preserveNullAndEmptyArrays": True}},
        # unir edicion -> libro
        {"$lookup": {
            "from": "libros",
            "localField": "edicion.libro_id",
            "foreignField": "_id",
            "as": "libro"
        }},
        {"$unwind": {"path": "$libro", "preserveNullAndEmptyArrays": True}},
        # unir libro -> autor
        {"$lookup": {
            "from": "autores",
            "localField": "libro.autor_id",
            "foreignField": "_id",
            "as": "autor"
        }},
        {"$unwind": {"path": "$autor", "preserveNullAndEmptyArrays": True}},
        # proyectar campos
        {"$project": {
            "_id": 1,
            "codigo_copia": 1,
            "estado": 1,
            "ubicacion": 1,
            "edicion": {"isbn": "$edicion.isbn", "editorial": "$edicion.editorial", "anio": "$edicion.anio"},
            "libro": {"titulo": "$libro.titulo", "genero": "$libro.genero", "anio_publicacion": "$libro.anio_publicacion"},
            "autor": {"nombre": "$autor.nombre", "apellido": "$autor.apellido", "pais": "$autor.pais"}
        }}
    ]

    res = list(db.copias.aggregate(pipeline))
    # convertir _id a string
    for r in res:
        r["_id"] = str(r["_id"])
    return jsonify(res), 200

@bp.route("/libros_prestados_por_usuario/<usuario_documento>", methods=["GET"])
def libros_prestados_por_usuario(usuario_documento):
    db = current_app.config["DB"]
    # Encontrar usuario por documento
    usuario = db.usuarios.find_one({"documento": usuario_documento})
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    usuario_id = usuario["_id"]

    pipeline = [
        {"$match": {"usuario_id": usuario_id}},
        {"$lookup": {
            "from": "copias",
            "localField": "copia_id",
            "foreignField": "_id",
            "as": "copia"
        }},
        {"$unwind": {"path": "$copia", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "ediciones",
            "localField": "copia.edicion_id",
            "foreignField": "_id",
            "as": "edicion"
        }},
        {"$unwind": {"path": "$edicion", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "libros",
            "localField": "edicion.libro_id",
            "foreignField": "_id",
            "as": "libro"
        }},
        {"$unwind": {"path": "$libro", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 1,
            "fecha_prestamo": 1,
            "fecha_devolucion_estimada": 1,
            "fecha_devolucion_real": 1,
            "estado": 1,
            "libro": {"titulo": "$libro.titulo", "genero": "$libro.genero"},
            "copia": {"codigo_copia": "$copia.codigo_copia"}
        }}
    ]

    res = list(db.prestamos.aggregate(pipeline))
    for r in res:
        r["_id"] = str(r["_id"])
    return jsonify(res), 200
