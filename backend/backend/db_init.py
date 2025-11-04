from pymongo import MongoClient, ASCENDING
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def create_collections():
    # Nombres: autores, libros, ediciones, copias, usuarios, prestamos
    db.create_collection("autores" )
    db.create_collection("libros")
    db.create_collection("ediciones")
    db.create_collection("copias")
    db.create_collection("usuarios")
    db.create_collection("prestamos")

    # Índices útiles (ejemplo)
    db.autores.create_index([("apellido", ASCENDING)], name="idx_autor_apellido")
    db.libros.create_index([("titulo", ASCENDING)], name="idx_libro_titulo")
    db.ediciones.create_index([("isbn", ASCENDING)], name="idx_edicion_isbn", unique=True)
    db.copias.create_index([("codigo_copia", ASCENDING)], name="idx_copia_codigo", unique=True)
    db.usuarios.create_index([("documento", ASCENDING)], name="idx_usuario_documento", unique=True)
    db.prestamos.create_index([("usuario_id", ASCENDING)], name="idx_prestamo_usuario")
    print("Colecciones e índices creados.")

def insert_sample_data():
    # AUTOR
    autor_id = db.autores.insert_one({
        "nombre": "Gabriel",
        "apellido": "García Márquez",
        "pais": "Colombia",
        "nacimiento": "1927-03-06"
    }).inserted_id

    libro_id = db.libros.insert_one({
        "titulo": "Cien años de soledad",
        "autor_id": autor_id,
        "genero": "Novela",
        "anio_publicacion": 1967
    }).inserted_id

    edicion_id = db.ediciones.insert_one({
        "libro_id": libro_id,
        "isbn": "978-0307474728",
        "editorial": "Sudamericana",
        "anio": 2003,
        "formato": "Tapa blanda"
    }).inserted_id

    copia_id = db.copias.insert_one({
        "edicion_id": edicion_id,
        "codigo_copia": "C-0001",
        "estado": "Disponible",
        "ubicacion": "Estantería 1"
    }).inserted_id

    usuario_id = db.usuarios.insert_one({
        "nombre": "Juan",
        "apellido": "Pérez",
        "documento": "1098765432",
        "telefono": "3001234567",
        "email": "juan@example.com"
    }).inserted_id

    prestamos_id = db.prestamos.insert_one({
        "usuario_id": usuario_id,
        "copia_id": copia_id,
        "fecha_prestamo": "2025-10-01",
        "fecha_devolucion_estimada": "2025-10-15",
        "fecha_devolucion_real": None,
        "estado": "Prestado"
    }).inserted_id

    print("Datos de ejemplo insertados.")

if __name__ == "__main__":
    create_collections()
    insert_sample_data()
