# menu.py
import os
import requests
import urllib.parse

API = os.getenv("API_URL", "http://localhost:5000")

def input_json(prompt):
    import json
    s = input(prompt)
    try:
        return json.loads(s)
    except:
        print("Error: el input debe ser JSON válido.")
        return None

def menu_principal():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1) Autores (CRUD)")
        print("2) Libros (CRUD)")
        print("3) Ediciones (CRUD)")
        print("4) Copias (CRUD)")
        print("5) Usuarios (CRUD)")
        print("6) Prestamos")
        print("7) Consultas")
        print("0) Salir")
        opt = input("> ").strip()
        if opt == "1":
            menu_autores()
        elif opt == "2":
            menu_libros()
        elif opt == "3":
            menu_ediciones()
        elif opt == "4":
            menu_copias()
        elif opt == "5":
            menu_usuarios()
        elif opt == "6":
            menu_prestamos()
        elif opt == "7":
            menu_consultas()
        elif opt == "0":
            break

def menu_autores():
    while True:
        print("\n--- AUTORES ---")
        print("1) Crear (JSON: {\"nombre\":\"...\"})")
        print("2) Listar")
        print("3) Obtener por nombre")
        print("4) Actualizar (PUT JSON)")
        print("5) Eliminar")
        print("0) Volver")
        op = input("> ")
        if op == "1":
            j = input_json("JSON: ")
            if j: print(requests.post(f"{API}/autores/", json=j).json())
        elif op == "2":
            print(requests.get(f"{API}/autores/").json())
        elif op == "3":
            nombre = input("nombre: ")
            print(requests.get(f"{API}/autores/{urllib.parse.quote(nombre)}").json())
        elif op == "4":
            nombre = input("nombre actual: ")
            j = input_json("PUT JSON: ")
            if j: print(requests.put(f"{API}/autores/{urllib.parse.quote(nombre)}", json=j).json())
        elif op == "5":
            nombre = input("nombre: ")
            print(requests.delete(f"{API}/autores/{urllib.parse.quote(nombre)}").json())
        else:
            break

def menu_libros():
    while True:
        print("\n--- LIBROS ---")
        print("1) Crear (JSON: {\"titulo\":\"...\",\"autores\":[...]})")
        print("2) Listar")
        print("3) Obtener por titulo")
        print("4) Actualizar (PUT JSON)")
        print("5) Eliminar")
        print("0) Volver")
        op = input("> ")
        if op == "1":
            j = input_json("JSON: ")
            if j: print(requests.post(f"{API}/libros/", json=j).json())
        elif op == "2":
            print(requests.get(f"{API}/libros/").json())
        elif op == "3":
            titulo = input("titulo: ")
            print(requests.get(f"{API}/libros/{urllib.parse.quote(titulo)}").json())
        elif op == "4":
            titulo = input("titulo actual: ")
            j = input_json("PUT JSON: ")
            if j: print(requests.put(f"{API}/libros/{urllib.parse.quote(titulo)}", json=j).json())
        elif op == "5":
            titulo = input("titulo: ")
            print(requests.delete(f"{API}/libros/{urllib.parse.quote(titulo)}").json())
        else:
            break

def menu_ediciones():
    while True:
        print("\n--- EDICIONES ---")
        print("1) Crear (JSON: {\"ISBN\":\"...\",\"titulo\":\"...\",\"anio\":2000,\"idioma\":\"...\"})")
        print("2) Listar")
        print("3) Obtener por ISBN")
        print("4) Actualizar (PUT JSON)")
        print("5) Eliminar")
        print("0) Volver")
        op = input("> ")
        if op == "1":
            j = input_json("JSON: ")
            if j: print(requests.post(f"{API}/ediciones/", json=j).json())
        elif op == "2":
            print(requests.get(f"{API}/ediciones/").json())
        elif op == "3":
            isbn = input("ISBN: ")
            print(requests.get(f"{API}/ediciones/{urllib.parse.quote(isbn)}").json())
        elif op == "4":
            isbn = input("ISBN: ")
            j = input_json("PUT JSON: ")
            if j: print(requests.put(f"{API}/ediciones/{urllib.parse.quote(isbn)}", json=j).json())
        elif op == "5":
            isbn = input("ISBN: ")
            print(requests.delete(f"{API}/ediciones/{urllib.parse.quote(isbn)}").json())
        else:
            break

def menu_copias():
    while True:
        print("\n--- COPIAS ---")
        print("1) Crear (JSON: {\"ISBN\":\"...\",\"numero\":1})")
        print("2) Listar")
        print("3) Obtener por ISBN/numero")
        print("4) Actualizar (PUT JSON)")
        print("5) Eliminar")
        print("0) Volver")
        op = input("> ")
        if op == "1":
            j = input_json("JSON: ")
            if j: print(requests.post(f"{API}/copias/", json=j).json())
        elif op == "2":
            print(requests.get(f"{API}/copias/").json())
        elif op == "3":
            isbn = input("ISBN: "); num = input("numero: ")
            print(requests.get(f"{API}/copias/{urllib.parse.quote(isbn)}/{int(num)}").json())
        elif op == "4":
            isbn = input("ISBN: "); num = input("numero: ")
            j = input_json("PUT JSON: ")
            if j: print(requests.put(f"{API}/copias/{urllib.parse.quote(isbn)}/{int(num)}", json=j).json())
        elif op == "5":
            isbn = input("ISBN: "); num = input("numero: ")
            print(requests.delete(f"{API}/copias/{urllib.parse.quote(isbn)}/{int(num)}").json())
        else:
            break

def menu_usuarios():
    while True:
        print("\n--- USUARIOS ---")
        print("1) Crear (JSON: {\"RUT\":\"...\",\"nombre\":\"...\"})")
        print("2) Listar")
        print("3) Obtener por RUT")
        print("4) Actualizar (PUT JSON)")
        print("5) Eliminar")
        print("0) Volver")
        op = input("> ")
        if op == "1":
            j = input_json("JSON: ")
            if j: print(requests.post(f"{API}/usuarios/", json=j).json())
        elif op == "2":
            print(requests.get(f"{API}/usuarios/").json())
        elif op == "3":
            rut = input("RUT: ")
            print(requests.get(f"{API}/usuarios/{urllib.parse.quote(rut)}").json())
        elif op == "4":
            rut = input("RUT: ")
            j = input_json("PUT JSON: ")
            if j: print(requests.put(f"{API}/usuarios/{urllib.parse.quote(rut)}", json=j).json())
        elif op == "5":
            rut = input("RUT: ")
            print(requests.delete(f"{API}/usuarios/{urllib.parse.quote(rut)}").json())
        else:
            break

def menu_prestamos():
    while True:
        print("\n--- PRÉSTAMOS ---")
        print("1) Crear préstamo")
        print("2) Listar préstamos")
        print("3) Buscar préstamo")
        print("4) Actualizar préstamo")
        print("5) Eliminar préstamo")
        print("0) Volver")
        op = input("> ")

        # 1. CREAR
        if op == "1":
            print("\nEjemplo de JSON:")
            print('{"RUT":"12345678-9","ISBN":"978-0307474728","numero":1,"Fecha_prestamo":"2025-11-03","Fecha_devolucion":"2025-11-15"}')
            j = input_json("Ingrese JSON: ")
            if j:
                print(requests.post(f"{API}/prestamos/", json=j).json())

        # 2. LISTAR
        elif op == "2":
            print(requests.get(f"{API}/prestamos/").json())

        # 3. BUSCAR
        elif op == "3":
            RUT = input("RUT (opcional): ").strip()
            ISBN = input("ISBN (opcional): ").strip()
            numero = input("Número de copia (opcional): ").strip()

            params = {}
            if RUT: params["RUT"] = RUT
            if ISBN: params["ISBN"] = ISBN
            if numero: params["numero"] = numero

            print(requests.get(f"{API}/prestamos/buscar", params=params).json())

        # 4. ACTUALIZAR
        elif op == "4":
            print("\nPrimero debes indicar qué préstamo vas a modificar")
            RUT = input("RUT: ").strip()
            ISBN = input("ISBN: ").strip()
            numero = input("Número de copia: ").strip()

            print("\nEjemplo de JSON (solo lo que deseas modificar):")
            print('{"Fecha_devolucion":"2025-11-20"}')
            j = input_json("Ingrese JSON: ")

            if j:
                # Añadir los campos clave para identificar el préstamo
                j["RUT"] = RUT
                j["ISBN"] = ISBN
                j["numero"] = int(numero)

                print(requests.put(f"{API}/prestamos/actualizar", json=j).json())

        # 5. ELIMINAR
        elif op == "5":
            RUT = input("RUT: ").strip()
            ISBN = input("ISBN: ").strip()
            numero = input("Número de copia: ").strip()

            data = {"RUT": RUT, "ISBN": ISBN, "numero": int(numero)}
            print(requests.delete(f"{API}/prestamos/eliminar", json=data).json())

        else:
            break


def menu_consultas():
    while True:
        print("\n--- CONSULTAS ---")
        print("1) Copias con detalle (edicion + libro + autores)")
        print("2) Libros prestados por usuario (por RUT)")
        print("0) Volver")
        op = input("> ")
        if op == "1":
            print(requests.get(f"{API}/consultas/copias_con_detalle").json())
        elif op == "2":
            rut = input("RUT: ")
            print(requests.get(f"{API}/consultas/libros_prestados_por_usuario/{urllib.parse.quote(rut)}").json())
        else:
            break

if __name__ == "__main__":
    menu_principal()
