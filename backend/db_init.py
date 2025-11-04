from pymongo import MongoClient, ASCENDING
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def create_collection_if_not_exists(name):
    """Crea la colección solo si no existe en la BD."""
    existing_collections = db.list_collection_names()
    if name not in existing_collections:
        db.create_collection(name)
        print(f" Colección creada: {name}")
    else:
        print(f" Colección ya existe: {name}")

def create_collections():
    collections = ["autores", "libros", "ediciones", "copias", "usuarios", "prestamos"]
    for name in collections:
        create_collection_if_not_exists(name)

    # Índices únicos para PKs naturales
    db.autor.create_index([("nombre", ASCENDING)], name="uq_autor_nombre", unique=True)
    db.libro.create_index([("titulo", ASCENDING)], name="uq_libro_titulo", unique=True)
    db.edicion.create_index([("ISBN", ASCENDING)], name="uq_edicion_ISBN", unique=True)
    db.usuario.create_index([("RUT", ASCENDING)], name="uq_usuario_RUT", unique=True)
    # Índice compuesto único para copias (entidad débil)
    db.copia.create_index([("ISBN", ASCENDING), ("numero", ASCENDING)], name="uq_copia_ISBN_numero", unique=True)
    # Índice para facilitar consultas de préstamos
    db.prestamo.create_index([("RUT", ASCENDING)], name="idx_prestamo_RUT")
    db.prestamo.create_index([("ISBN", ASCENDING), ("numero", ASCENDING)], name="idx_prestamo_copia")

    print("\n Colecciones e índices listos.\n")


def insert_sample_data():
    # Insertar ejemplo solo si no existe la edición de ejemplo
    if db.ediciones.find_one({"ISBN": "978-0307474728"}):
        print("ℹ️ Datos de ejemplo ya existen. No se insertarán nuevos datos.")
        return

    # Autor (PK: nombre)
    try:
        db.autores.insert_one({"nombre": "Gabriel García Márquez"})
    except Exception:
        pass

    # Libro (PK: titulo, autores: array de nombres)
    try:
        db.libros.insert_one({
            "titulo": "Cien años de soledad",
            "autores": ["Gabriel García Márquez"]
        })
    except Exception:
        pass

    # Edicion (PK: ISBN, referencia a libro por titulo)
    try:
        db.ediciones.insert_one({
            "ISBN": "978-0307474728",
            "titulo": "Cien años de soledad",
            "anio": 2003,
            "idioma": "Español"
        })
    except Exception:
        pass

    # Copia (entidad débil) - clave parcial numero + ISBN
    try:
        db.copias.insert_one({
            "ISBN": "978-0307474728",
            "numero": 1
        })
    except Exception:
        pass

    # Usuario (PK: RUT)
    try:
        db.usuarios.insert_one({
            "RUT": "109876543-2",
            "nombre": "Juan Pérez"
        })
    except Exception:
        pass

    # Prestamo (relación)
    try:
        db.prestamos.insert_one({
            "RUT": "109876543-2",
            "ISBN": "978-0307474728",
            "numero": 1,
            "Fecha_prestamo": "2025-11-03",
            "Fecha_devolucion": "2025-11-15"
        })
    except Exception:
        pass

    print("✅ Datos de ejemplo insertados (o ya existían).")

if __name__ == "__main__":
    print("⏳ Inicializando base de datos...")
    create_collections()
    insert_sample_data()
    print("🎉 Base de datos lista.")
