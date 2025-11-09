from pymongo import MongoClient, ASCENDING
from config import MONGO_URI, DB_NAME
from datetime import datetime

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
    db.usuarios.delete_many({})
    db.autores.delete_many({})
    db.libros.delete_many({})
    db.ediciones.delete_many({})
    db.copias.delete_many({})
    db.prestamos.delete_many({})

    # -----------------------------
    # Datos de ejemplo
    # -----------------------------

    # Usuarios
    usuarios_data = [
        {"RUT": 101, "nombre": "Ana Pérez"},
        {"RUT": 102, "nombre": "Carlos Gómez"},
        {"RUT": 103, "nombre": "María Torres"},
    ]
    db.usuarios.insert_many(usuarios_data)

    # Autores
    autores_data = [
        {"nombre": "Gabriel García Márquez"},
        {"nombre": "J.K. Rowling"},
        {"nombre": "George Orwell"},
    ]
    db.autores.insert_many(autores_data)

    # Libros
    libros_data = [
        {
            "titulo": "Cien Años de Soledad",
            "autores": ["Gabriel García Márquez"]
        },
        {
            "titulo": "Harry Potter y la Piedra Filosofal",
            "autores": ["J.K. Rowling"]
        },
        {
            "titulo": "1984",
            "autores": ["George Orwell"]
        }
    ]
    db.libros.insert_many(libros_data)

    # Ediciones
    ediciones_data = [
        {"ISBN": "9780307474728", "titulo": "Cien Años de Soledad", "anio": 1967, "idioma": "Español"},
        {"ISBN": "9788478884452", "titulo": "Harry Potter y la Piedra Filosofal", "anio": 1997, "idioma": "Español"},
        {"ISBN": "9780451524935", "titulo": "1984", "anio": 1949, "idioma": "Inglés"}
    ]
    db.ediciones.insert_many(ediciones_data)

    # Copias
    copias_data = [
        {"ISBN": "9780307474728", "numero": 1},
        {"ISBN": "9780307474728", "numero": 2},
        {"ISBN": "9788478884452", "numero": 1},
        {"ISBN": "9780451524935", "numero": 1},
    ]
    db.copias.insert_many(copias_data)

    # Préstamos
    prestamos_data = [
        {
            "RUT": 101,
            "ISBN": "9780307474728",
            "numero": 1,
            "fecha_prestamo": "2025-11-01",
            "fecha_devolucion": "2025-11-10"
        },
        {
            "RUT": 102,
            "ISBN": "9788478884452",
            "numero": 1,
            "fecha_prestamo": "2025-11-02",
            "fecha_devolucion": "2025-11-09"
        },
        {
            "RUT": 103,
            "ISBN": "9780451524935",
            "numero": 1,
            "fecha_prestamo": "2025-11-03",
            "fecha_devolucion": "2025-11-12"
        }
    ]
    db.prestamos.insert_many(prestamos_data)

    # -----------------------------
    # Confirmación
    # -----------------------------
    print("Datos insertados correctamente.")
    print(f"Usuarios: {db.usuarios.count_documents({})}")
    print(f"Autores: {db.autores.count_documents({})}")
    print(f"Libros: {db.libros.count_documents({})}")
    print(f"Ediciones: {db.ediciones.count_documents({})}")
    print(f"Copias: {db.copias.count_documents({})}")
    print(f"Préstamos: {db.prestamos.count_documents({})}")

if __name__ == "__main__":
    print("⏳ Inicializando base de datos...")
    create_collections()
    insert_sample_data()
    print("🎉 Base de datos lista.")
