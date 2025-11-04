from flask import Blueprint, current_app, jsonify

bp = Blueprint("consultas", __name__)

@bp.route("/copias_detalle", methods=["GET"])
def copias_detalle():
    db = current_app.config["DB"]
    pipeline = [
        {"$lookup": {"from":"ediciones","localField":"ISBN","foreignField":"ISBN","as":"edicion"}},
        {"$unwind":"$edicion"},
        {"$lookup": {"from":"libros","localField":"edicion.libro","foreignField":"titulo","as":"libro"}},
        {"$unwind":"$libro"},
        {"$lookup": {"from":"autores","localField":"libro.autores","foreignField":"nombre","as":"autores"}},
        {"$project":{"_id":0,"ISBN":1,"numero":1,"libro":"$libro.titulo","autores":"$autores.nombre","año":"$edicion.año","idioma":"$edicion.idioma"}}
    ]
    return jsonify(list(db.copias.aggregate(pipeline))), 200


@bp.route("/prestamos_usuario/<rut>", methods=["GET"])
def usuario_libros(rut):
    db = current_app.config["DB"]
    pipeline = [
        {"$match":{"rut":rut}},
        {"$lookup":{"from":"ediciones","localField":"ISBN","foreignField":"ISBN","as":"edicion"}},
        {"$unwind":"$edicion"},
        {"$lookup":{"from":"libros","localField":"edicion.libro","foreignField":"titulo","as":"libro"}},
        {"$unwind":"$libro"},
        {"$project":{"_id":0,"ISBN":1,"numero":1,"fecha_prestamo":1,"fecha_devolucion":1,"titulo":"$libro.titulo","autores":"$libro.autores"}}
    ]
    return jsonify(list(db.prestamos.aggregate(pipeline))), 200
