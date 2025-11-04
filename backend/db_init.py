from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "biblioteca_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def create_collections():
    for col in ["usuarios","autores","libros","ediciones","copias","prestamos"]:
        if col in db.list_collection_names():
            db[col].drop()
        db.create_collection(col)

    db.usuarios.create_index("rut", unique=True)
    db.ediciones.create_index("ISBN", unique=True)
    db.copias.create_index([("ISBN",1),("numero",1)], unique=True)


def insert_sample():
    db.usuarios.insert_many([
        {"rut":"123","nombre":"Juan"},
        {"rut":"456","nombre":"Ana"}
    ])
    
    db.autores.insert_many([
        {"nombre":"Gabriel García Márquez"},
        {"nombre":"Isabel Allende"}
    ])

    db.libros.insert_many([
        {"titulo":"Cien años de soledad","autores":["Gabriel García Márquez"]},
        {"titulo":"La casa de los espiritus","autores":["Isabel Allende"]}
    ])

    db.ediciones.insert_many([
        {"ISBN":"ISBN001","libro":"Cien años de soledad","año":1967,"idioma":"Español"},
        {"ISBN":"ISBN002","libro":"La casa de los espiritus","año":1982,"idioma":"Español"}
    ])

    db.copias.insert_many([
        {"ISBN":"ISBN001","numero":1},
        {"ISBN":"ISBN001","numero":2},
        {"ISBN":"ISBN002","numero":1}
    ])

    db.prestamos.insert_one(
        {"rut":"123","ISBN":"ISBN001","numero":1,"fecha_prestamo":"2025-01-01","fecha_devolucion":None}
    )


if __name__ == "__main__":
    create_collections()
    insert_sample()
    print("Base de datos inicializada ")
