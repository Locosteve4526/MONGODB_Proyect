from flask import Blueprint, current_app, jsonify, request
from bson.objectid import ObjectId

bp = Blueprint("consultas", __name__)

def db():
    return current_app.config["DB"]

@bp.route("/copias_con_detalle", methods=["GET"])
def copias_con_detalle():
    pipeline = [
        {"$lookup": {
            "from": "ediciones",
            "localField": "ISBN",
            "foreignField": "ISBN",
            "as": "ed"
        }},
        {"$unwind": {"path": "$ed", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "libros",
            "localField": "ed.titulo",
            "foreignField": "titulo",
            "as": "lib"
        }},
        {"$unwind": {"path": "$lib", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 0,
            "ISBN": 1, "numero": 1,
            "edicion": {"ISBN": "$ed.ISBN", "anio": "$ed.anio", "idioma": "$ed.idioma"},
            "libro": {"titulo": "$lib.titulo", "autores": "$lib.autores"}
        }}
    ]
    res = list(db().copias.aggregate(pipeline))
    return jsonify(res), 200

@bp.route("/libros_prestados_por_usuario/<string:RUT>", methods=["GET"])
def libros_prestados_por_usuario(RUT):
    pipeline = [
        {"$match": {"RUT": RUT}},
        {"$lookup": {
            "from": "ediciones",
            "localField": "ISBN",
            "foreignField": "ISBN",
            "as": "ed"
        }},
        {"$unwind": {"path": "$ed", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "libros",
            "localField": "ed.titulo",
            "foreignField": "titulo",
            "as": "lib"
        }},
        {"$unwind": {"path": "$lib", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 0,
            "RUT": 1, "ISBN": 1, "numero": 1, "Fecha_prestamo": 1, "Fecha_devolucion": 1,
            "libro": {"titulo": "$lib.titulo", "autores": "$lib.autores"},
            "edicion": {"ISBN": "$ed.ISBN", "anio": "$ed.anio", "idioma": "$ed.idioma"}
        }}
    ]
    res = list(db().prestamos.aggregate(pipeline))
    return jsonify(res), 200