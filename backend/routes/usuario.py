from flask import Blueprint, request, current_app, jsonify
from bson.objectid import ObjectId

bp = Blueprint("usuarios", __name__)

def col():
    return current_app.config["DB"].usuarios

@bp.route("/", methods=["OPTIONS"])
def handle_options():
    return "", 204

@bp.route("/", methods=["POST"])
def crear_usuario():
    try:
        data = request.json or {}
        print(f"📥 Datos recibidos para crear usuario: {data}")
        
        RUT = (data.get("rut") or "").strip()
        nombre = (data.get("nombre") or "").strip()
        
        if not RUT or not nombre:
            return jsonify({"error": "Faltan RUT o nombre"}), 400
        
        if col().find_one({"rut": RUT}):
            return jsonify({"error": "Usuario ya existe"}), 400
        
        col().insert_one({"rut": RUT, "nombre": nombre})
        print(f"✅ Usuario creado: RUT={RUT}, nombre={nombre}")
        return jsonify({"msg": "Usuario creado", "RUT": RUT}), 201
    except Exception as e:
        print(f"❌ Error creando usuario: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/", methods=["GET"])
def listar_usuarios():
    try:
        docs = list(col().find({}, {"_id": 0}))
        print(f"📋 Listando {len(docs)} usuarios")
        return jsonify(docs), 200
    except Exception as e:
        print(f"❌ Error listando usuarios: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/<string:RUT>", methods=["OPTIONS"])
def handle_options_with_rut(RUT):
    return "", 204

@bp.route("/<string:RUT>", methods=["GET"])
def obtener_usuario(RUT):
    try:
        doc = col().find_one({"RUT": RUT}, {"_id": 0})
        if not doc:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(doc), 200
    except Exception as e:
        print(f"❌ Error obteniendo usuario: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/<string:RUT>", methods=["PUT"])
def actualizar_usuario(RUT):
    try:
        data = request.json or {}
        print(f"📝 Actualizando usuario {RUT} con datos: {data}")
        
        # Si se intenta cambiar el RUT, verificar que no exista
        if "RUT" in data and data["RUT"] != RUT:
            if col().find_one({"RUT": data["RUT"]}):
                return jsonify({"error": "Nuevo RUT ya existe"}), 400
        
        res = col().update_one({"RUT": RUT}, {"$set": data})
        
        if res.matched_count == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        print(f"✅ Usuario {RUT} actualizado")
        return jsonify({"msg": "Usuario actualizado"}), 200
    except Exception as e:
        print(f"❌ Error actualizando usuario: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/<string:RUT>", methods=["DELETE"])
def borrar_usuario(RUT):
    try:
        print(f"🗑️ Intentando eliminar usuario: {RUT}")
        res = col().delete_one({"rut": RUT})
        
        if res.deleted_count == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        print(f"✅ Usuario {RUT} eliminado")
        return jsonify({"msg": "Usuario eliminado"}), 200
    except Exception as e:
        print(f"❌ Error eliminando usuario: {str(e)}")
        return jsonify({"error": str(e)}), 500
