import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def pedir(texto):
    return input(f"{texto}: ").strip()

def menu_usuarios():
    while True:
        print("\n--- USUARIOS ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Buscar usuario")
        print("4. Eliminar usuario")
        print("0. Volver")
        op = pedir("Opción")

        if op=="1":
            data = {"rut": pedir("RUT"), "nombre": pedir("Nombre")}
            r = requests.post(f"{BASE_URL}/usuarios/", json=data)
            print(r.json())

        elif op=="2":
            print(requests.get(f"{BASE_URL}/usuarios/").json())

        elif op=="3":
            rut = pedir("RUT")
            print(requests.get(f"{BASE_URL}/usuarios/{rut}").json())

        elif op=="4":
            rut = pedir("RUT")
            print(requests.delete(f"{BASE_URL}/usuarios/{rut}").json())

        elif op=="0": break


def menu_autores():
    while True:
        print("\n--- AUTORES ---")
        print("1. Crear autor")
        print("2. Listar autores")
        print("0. Volver")
        op = pedir("Opción")

        if op=="1":
            data = {"nombre": pedir("Nombre")}
            print(requests.post(f"{BASE_URL}/autores/", json=data).json())

        elif op=="2":
            print(requests.get(f"{BASE_URL}/autores/").json())

        elif op=="0": break


def menu_libros():
    while True:
        print("\n--- LIBROS ---")
        print("1. Crear libro")
        print("2. Listar libros")
        print("0. Volver")
        op = pedir("Opción")

        if op=="1":
            titulo = pedir("Título del libro")
            autores = pedir("Autores (separados por coma)").split(",")
            autores = [a.strip() for a in autores]
            data = {"titulo": titulo, "autores": autores}
            print(requests.post(f"{BASE_URL}/libros/", json=data).json())

        elif op=="2":
            print(requests.get(f"{BASE_URL}/libros/").json())

        elif op=="0": break


def menu_ediciones():
    while True:
        print("\n--- EDICIONES ---")
        print("1. Crear edición")
        print("2. Listar ediciones")
        print("0. Volver")
        op = pedir("Opción")

        if op=="1":
            data = {
                "ISBN": pedir("ISBN"),
                "libro": pedir("Título del libro (ya registrado)"),
                "año": int(pedir("Año")),
                "idioma": pedir("Idioma"),
            }
            print(requests.post(f"{BASE_URL}/ediciones/", json=data).json())

        elif op=="2":
            print(requests.get(f"{BASE_URL}/ediciones/").json())

        elif op=="0": break


def menu_copias():
    while True:
        print("\n--- COPIAS ---")
        print("1. Crear copia")
        print("2. Listar copias")
        print("3. Buscar copia")
        print("4. Eliminar copia")
        print("0. Volver")
        op = pedir("Opción")

        if op=="1":
            data = {"ISBN": pedir("ISBN"), "numero": int(pedir("Número de copia"))}
            print(requests.post(f"{BASE_URL}/copias/", json=data).json())

        elif op=="2":
            print(requests.get(f"{BASE_URL}/copias/").json())

        elif op=="3":
            isbn = pedir("ISBN")
            num = pedir("Número de copia")
            print(requests.get(f"{BASE_URL}/copias/{isbn}/{num}").json())

        elif op=="4":
            isbn = pedir("ISBN")
            num = pedir("Número de copia")
            print(requests.delete(f"{BASE_URL}/copias/{isbn}/{num}").json())

        elif op=="0": break


def menu_prestamos():
    while True:
        print("\n--- PRÉSTAMOS ---")
        print("1. Registrar préstamo")
        print("2. Devolver libro")
        print("3. Lista de préstamos")
        print("0. Volver")
        op = pedir("Opción")

        if op=="1":
            data = {
                "rut": pedir("RUT usuario"),
                "ISBN": pedir("ISBN"),
                "numero": int(pedir("Número de copia")),
            }
            print(requests.post(f"{BASE_URL}/prestamos/", json=data).json())

        elif op=="2":
            data = {
                "rut": pedir("RUT usuario"),
                "ISBN": pedir("ISBN"),
                "numero": int(pedir("Número de copia")),
            }
            print(requests.post(f"{BASE_URL}/prestamos/devolver", json=data).json())

        elif op=="3":
            print(requests.get(f"{BASE_URL}/prestamos/").json())

        elif op=="0": break


def main():
    while True:
        print("\n=== BIBLIOTECA — MENU PRINCIPAL ===")
        print("1. Usuarios")
        print("2. Autores")
        print("3. Libros")
        print("4. Ediciones")
        print("5. Copias")
        print("6. Préstamos")
        print("0. Salir")
        op = pedir("Opción")

        if op=="1": menu_usuarios()
        elif op=="2": menu_autores()
        elif op=="3": menu_libros()
        elif op=="4": menu_ediciones()
        elif op=="5": menu_copias()
        elif op=="6": menu_prestamos()
        elif op=="0":
            print("Saliendo...")
            break


if __name__ == "__main__":
    main()
