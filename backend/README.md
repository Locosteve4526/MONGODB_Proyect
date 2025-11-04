# Proyecto CRUD Biblioteca (Modelo según diagrama)

## Resumen
Backend en Python + Flask con MongoDB. Modelo fiel al diagrama: PK naturales, copias como entidad débil, colecciones y rutas en plural.

## Estructura (raíz)
- app.py
- config.py
- db_init.py
- requirements.txt
- .env
- README.md
- menu.py
- routes/
  - autor.py
  - libro.py
  - edicion.py
  - copia.py
  - usuario.py
  - prestamo.py
  - consultas.py

> Nota: archivos en `routes/` se mantienen con nombre singular para tu conveniencia, pero las rutas y colecciones son **plurales** (/autores, /libros, /ediciones, /copias, /usuarios, /prestamos).

## Requisitos
- Python 3.10+
- MongoDB local o Atlas

## Instalación rápida
1. Crear y activar entorno virtual:
   - Windows PowerShell:
     ```
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
2. Instalar dependencias:
  pip install -r requirements.txt
3. Configurar `.env` con `MONGO_URI` y `DB_NAME`.

## Inicializar BD y datos de ejemplo
python db_init.py

## Ejecutar API
python app.py
API en `http://localhost:5000/`

## Ejecutar menú por consola (en otra terminal con venv)
python menu.py

## Rutas principales (resumen)
- POST /autores/ — crear autor { "nombre": "..." }
- GET /autores/ — listar autores
- GET /autores/{nombre} — obtener autor
- POST /libros/ — crear libro { "titulo":"...","autores":["..."] }
- POST /ediciones/ — crear edicion { "ISBN":"...","titulo":"...","anio":2020,"idioma":"..."}
- POST /copias/ — crear copia { "ISBN":"...","numero":1 }
- POST /usuarios/ — crear usuario { "RUT":"...","nombre":"..." }
- POST /prestamos/ — crear prestamo { "RUT":"...","ISBN":"...","numero":1,"Fecha_prestamo":"YYYY-MM-DD","Fecha_devolucion":"YYYY-MM-DD" }
- GET /consultas/copias_con_detalle
- GET /consultas/libros_prestados_por_usuario/{RUT}

## Notas
- Las claves naturales son únicas (se crearon índices únicos).
- Copia tiene índice compuesto único `{ISBN, numero}`.
- Validaciones FK implementadas: no puedes crear una edición sin libro, ni una copia sin edición, etc.
