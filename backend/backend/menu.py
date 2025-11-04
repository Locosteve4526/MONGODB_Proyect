import requests
import os

API = os.getenv("API_URL", "http://localhost:5000")

def menu_principal():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1) AUTOR / LIBRO / EDICIÓN / COPIA (CRUD)")
        print("2) USUARIO (CRUD)")
        print("3) PRÉSTAMO (CRUD + devoluciones)")
        print("4) Consultas")
        print("0) Salir")
        opt = input("Elige opción: ").strip()
        if opt == "1":
            menu_biblioteca()
        elif opt == "2":
            menu_usuarios()
        elif opt == "3":
            menu_prestamos()
        elif opt == "4":
            menu_consultas()
        elif opt == "0":
            break
        else:
            print("Opción inválida.")

# Implementa submenús que llaman a endpoints (ejemplo para autores, similar para demás)
def menu_biblioteca():
    while True:
        print("\n--- AUTOR / LIBRO / EDICIÓN / COPIA ---")
        print("1) Crear autor")
        print("2) Listar autores")
        print("0) Volver")
        opt = input("op: ").strip()
        if opt == "1":
            nombre = input("nombre: ")
            apellido = input("apellido: ")
            pais = input("pais: ")
            payload = {"nombre": nombre, "apellido": apellido, "pais": pais}
            r = requests.post(f"{API}/autores/", json=payload)
            print(r.json())
        elif opt == "2":
            r = requests.get(f"{API}/autores/")
            print(r.json())
        elif opt == "0":
            break
        else:
            print("inválido")

def menu_usuarios():
    while True:
        print("\n--- USUARIOS ---")
        print("1) Crear usuario")
        print("2) Listar usuarios")
        print("0) Volver")
        opt = input("op: ").strip()
        if opt == "1":
            nombre = input("nombre: "); apellido = input("apellido: ")
            documento = input("documento: "); email = input("email: ")
            payload = {"nombre":nombre,"apellido":apellido,"documento":documento,"email":email}
            r = requests.post(f"{API}/usuarios/", json=payload)
            print(r.json())
        elif opt == "2":
            r = requests.get(f"{API}/usuarios/")
            print(r.json())
        elif opt == "0":
            break

def menu_prestamos():
    while True:
        print("\n--- PRÉSTAMOS ---")
        print("1) Crear préstamo")
        print("2) Devolver préstamo")
        print("3) Listar préstamos")
        print("0) Volver")
        opt = input("op: ").strip()
        if opt == "1":
            usuario_id = input("usuario_id (ObjectId): ")
            copia_id = input("copia_id (ObjectId): ")
            fecha_prestamo = input("fecha_prestamo (YYYY-MM-DD): ")
            fecha_dev = input("fecha_devolucion_estimada (YYYY-MM-DD): ")
            payload = {"usuario_id": usuario_id, "copia_id": copia_id, "fecha_prestamo": fecha_prestamo, "fecha_devolucion_estimada": fecha_dev}
            r = requests.post(f"{API}/prestamos/", json=payload)
            print(r.json())
        elif opt == "2":
            prest_id = input("id préstamo: ")
            fecha = input("fecha_devolucion_real (YYYY-MM-DD): ")
            r = requests.post(f"{API}/prestamos/{prest_id}/devolver", json={"fecha_devolucion_real": fecha})
            print(r.json())
        elif opt == "3":
            r = requests.get(f"{API}/prestamos/")
            print(r.json())
        elif opt == "0":
            break

def menu_consultas():
    while True:
        print("\n--- CONSULTAS ---")
        print("1) Listado de copias con AUTOR/LIBRO/EDICIÓN")
        print("2) Libros prestados por usuario (buscar por documento)")
        print("0) Volver")
        opt = input("op: ")
        if opt == "1":
            r = requests.get(f"{API}/consultas/copias_con_detalle")
            print(r.json())
        elif opt == "2":
            doc = input("documento usuario: ")
            r = requests.get(f"{API}/consultas/libros_prestados_por_usuario/{doc}")
            print(r.json())
        elif opt == "0":
            break

if __name__ == "__main__":
    menu_principal()
