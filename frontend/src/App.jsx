import { useState, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import NavigationTab from "./components/NavigationTab";
import modeloER from "./assets/modeloER.jpg";
import { Table } from "./components/Table";
import { Modal } from "./components/Modal";

function App() {
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedTab, setSelection] = useState(null);
  const [rows, setRows] = useState([]);
  const [rowToEdit, setRowToEdit] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Estados para consultas
  const [selectedRUT, setSelectedRUT] = useState("");
  const [copiasList, setCopiasList] = useState([]);
  const [librosPrestados, setLibrosPrestados] = useState([]);
  const [loadingConsulta1, setLoadingConsulta1] = useState(false);
  const [loadingConsulta2, setLoadingConsulta2] = useState(false);

  // Mapeo de tabs a endpoints y tipos
  const tabConfig = {
    1: { endpoint: "/usuarios", type: "usuario", label: "usuario" },
    2: { endpoint: "/autores", type: "autor", label: "autor" },
    3: { endpoint: "/libros", type: "libro", label: "libro" },
    4: { endpoint: "/ediciones", type: "edicion", label: "edicion" },
    5: { endpoint: "/copias", type: "copia", label: "copia" },
    6: { endpoint: "/prestamos", type: "prestamo", label: "prestamo" },
  };

  // Fetch data cuando cambia el tab
  useEffect(() => {
    if (selectedTab !== null) {
      fetchData();
    }
  }, [selectedTab]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const config = tabConfig[selectedTab];
      const url = `http://localhost:5000${config.endpoint}/`;
      console.log(`🔍 Fetching from: ${url}`);

      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      console.log(`📡 Response status: ${response.status}`);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ Error response: ${errorText}`);
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log(`📦 Data received from backend:`, data);

      setRows(data);
    } catch (err) {
      const errorMsg = err.message.includes("Failed to fetch") 
        ? "No se puede conectar al servidor. Verifica que Flask esté corriendo en http://localhost:5000"
        : err.message;
      setError(errorMsg);
      console.error("❌ Error fetching data:", err);
      setRows([]);
    } finally {
      setLoading(false);
    }
  };

  const handleEditRow = (idx) => {
    setRowToEdit(idx);
    setModalOpen(true);
  };

  const handleDeleteRow = async (targetIndex) => {
    const config = tabConfig[selectedTab];
    const rowToDelete = rows[targetIndex];

    console.log("🗑️ Datos de la fila a eliminar:", rowToDelete);

    // Obtener el ID correcto según el tipo de entidad
    let nodeId;
    if (selectedTab === 1) {
      // Para usuarios, el backend busca por "rut" en minúscula
      nodeId = encodeURIComponent(rowToDelete.rut || rowToDelete.RUT);
    } else if (selectedTab === 2) {
      nodeId = encodeURIComponent(rowToDelete.nombre);
    } else if (selectedTab === 3) {
      nodeId = encodeURIComponent(rowToDelete.titulo);
    } else if (selectedTab === 4) {
      nodeId = encodeURIComponent(rowToDelete.ISBN);
    } else if (selectedTab === 5) {
      const isbn = encodeURIComponent(rowToDelete.ISBN);
      const numero = encodeURIComponent(rowToDelete.numero);
      nodeId = `${isbn}/${numero}`;
    } else if (selectedTab === 6) {
      const rut = encodeURIComponent(rowToDelete.rut || rowToDelete.RUT);
      const isbn = encodeURIComponent(rowToDelete.ISBN);
      const numero = encodeURIComponent(rowToDelete.numero);
      nodeId = `${rut}/${isbn}/${numero}`;
    }

    console.log("🗑️ Eliminando con ID codificado:", nodeId);
    console.log("🗑️ URL completa:", `http://localhost:5000${config.endpoint}/${nodeId}`);

    if (!confirm(`¿Estás seguro de eliminar este registro?`)) {
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:5000${config.endpoint}/${nodeId}`,
        { 
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          }
        }
      );

      console.log("📡 DELETE Response status:", response.status);

      if (!response.ok) {
        const errorData = await response.text();
        console.error("❌ Error response:", errorData);
        throw new Error(errorData || "Error al eliminar");
      }

      // Actualizar UI
      setRows(rows.filter((row, index) => index !== targetIndex));
      alert("¡Registro eliminado exitosamente!");
    } catch (err) {
      setError(err.message);
      console.error("❌ Error deleting:", err);
      alert(`Error al eliminar: ${err.message}`);
    }
  };

  const handleSubmit = async (newRow) => {
    const config = tabConfig[selectedTab];

    console.log("=== HANDLE SUBMIT ===");
    console.log("📥 Datos recibidos del formulario (newRow):", newRow);
    console.log("📋 Tipo de datos:", typeof newRow);
    console.log("🏷️ Tab seleccionado:", selectedTab, "- Entidad:", config.label);

    // Los datos ya vienen con los campos correctos del formulario
    const dataToSend = { ...newRow };
    console.log("📤 Datos a enviar (dataToSend):", dataToSend);
    console.log("📤 JSON stringified:", JSON.stringify(dataToSend, null, 2));

    try {
      if (rowToEdit === null) {
        // ========== CREAR NUEVO ==========
        console.log("➕ MODO: Creando nuevo registro");
        console.log("🔗 URL:", `http://localhost:5000${config.endpoint}/`);
        
        const response = await fetch(
          `http://localhost:5000${config.endpoint}/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dataToSend),
          }
        );

        console.log("📡 POST Response status:", response.status);
        console.log("📡 POST Response ok:", response.ok);

        if (!response.ok) {
          const responseText = await response.text();
          console.error("❌ Error response (texto):", responseText);
          
          let errorData;
          try {
            errorData = JSON.parse(responseText);
            console.error("❌ Error response (JSON):", errorData);
          } catch {
            errorData = { error: responseText };
          }
          
          throw new Error(errorData.error || responseText || `Error: ${response.status}`);
        }

        const responseData = await response.json();
        console.log("✅ Respuesta exitosa del servidor:", responseData);

        // Cerrar modal y recargar datos
        setModalOpen(false);
        setRowToEdit(null);
        await fetchData();
        alert("¡Registro creado exitosamente!");
      } else {
        // ========== ACTUALIZAR EXISTENTE ==========
        const rowData = rows[rowToEdit];
        console.log("📝 Datos del row original:", rowData);
        
        let nodeId;
        
        if (selectedTab === 1) {
          // Para usuarios, el backend busca por "RUT" en mayúscula para UPDATE
          nodeId = encodeURIComponent(rowData.rut || rowData.RUT);
        } else if (selectedTab === 2) {
          nodeId = encodeURIComponent(rowData.nombre);
        } else if (selectedTab === 3) {
          nodeId = encodeURIComponent(rowData.titulo);
        } else if (selectedTab === 4) {
          nodeId = encodeURIComponent(rowData.ISBN);
        } else if (selectedTab === 5) {
          const isbn = encodeURIComponent(rowData.ISBN);
          const numero = encodeURIComponent(rowData.numero);
          nodeId = `${isbn}/${numero}`;
        } else if (selectedTab === 6) {
          const rut = encodeURIComponent(rowData.rut || rowData.RUT);
          const isbn = encodeURIComponent(rowData.ISBN);
          const numero = encodeURIComponent(rowData.numero);
          nodeId = `${rut}/${isbn}/${numero}`;
        }

        console.log("🔄 Actualizando con ID:", nodeId);
        console.log("🔄 URL:", `http://localhost:5000${config.endpoint}/${nodeId}`);
        console.log("📝 Datos a actualizar:", dataToSend);

        const response = await fetch(
          `http://localhost:5000${config.endpoint}/${nodeId}`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dataToSend),
          }
        );

        console.log("📡 PUT Response status:", response.status);

        if (!response.ok) {
          const errorText = await response.text();
          console.error("❌ Error del servidor:", errorText);
          let errorData;
          try {
            errorData = JSON.parse(errorText);
          } catch {
            errorData = { error: errorText };
          }
          throw new Error(errorData.error || `Error: ${response.status}`);
        }

        // Cerrar modal y recargar datos
        setModalOpen(false);
        setRowToEdit(null);
        await fetchData();
        alert("¡Registro actualizado exitosamente!");
      }
    } catch (err) {
      setError(err.message);
      console.error("❌ Error submitting:", err);
      alert(`Error: ${err.message}`);
    }
  };

  // Obtener los campos del formulario según el tab
  const getFormFields = () => {
    if (selectedTab === null) return [];

    // Siempre usar campos consistentes, independientemente de si hay datos o no
    switch (selectedTab) {
      case 1: // Usuarios
        return ["RUT", "nombre"];
      case 2: // Autores
        return ["nombre"];
      case 3: // Libros
        return ["titulo", "autores"];
      case 4: // Ediciones
        return ["ISBN", "titulo", "anio", "idioma"];
      case 5: // Copias
        return ["ISBN", "numero"];
      case 6: // Préstamos
        return ["RUT", "ISBN", "numero", "Fecha_prestamo", "Fecha_devolucion"];
      default:
        return [];
    }
  };

  // ========== CONSULTA 1: Copias con detalle ==========
  const consultarCopiasDetalle = async () => {
    console.log("=== CONSULTA 1 INICIADA ===");
    
    setLoadingConsulta1(true);
    setCopiasList([]); // Limpiar datos anteriores
    
    try {
      const url = `http://localhost:5000/consultas/copias_con_detalle`;
      console.log("Fetching URL:", url);

      const response = await fetch(url);
      console.log("Response status:", response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error response:", errorText);
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Copias recibidas:", data);
      console.log("Cantidad de copias:", data.length);
      
      // Transformar datos si es necesario para aplanar objetos anidados
      const transformedData = data.map(item => {
        const flat = {
          ISBN: item.ISBN,
          numero: item.numero,
        };
        
        // Aplanar libro
        if (item.libro) {
          flat.libro_titulo = item.libro.titulo;
          flat.libro_autores = Array.isArray(item.libro.autores) 
            ? item.libro.autores.join(', ') 
            : item.libro.autores;
        }
        
        // Aplanar edicion
        if (item.edicion) {
          flat.edicion_ISBN = item.edicion.ISBN;
          flat.edicion_anio = item.edicion.anio;
          flat.edicion_idioma = item.edicion.idioma;
        }
        
        return flat;
      });

      setCopiasList(transformedData);
    } catch (err) {
      console.error("❌ Error consultando copias:", err);
      setCopiasList([]);
      alert("Error al consultar copias: " + err.message);
    } finally {
      setLoadingConsulta1(false);
    }
  };

  // ========== CONSULTA 2: Libros prestados por usuario ==========
  const consultarLibrosPrestados = async () => {
    console.log("=== CONSULTA 2 INICIADA ===");
    console.log("RUT:", selectedRUT);

    if (!selectedRUT) {
      alert("Por favor ingresa un RUT");
      return;
    }

    setLoadingConsulta2(true);
    setLibrosPrestados([]); // Limpiar datos anteriores
    
    try {
      const url = `http://localhost:5000/consultas/libros_prestados_por_usuario/${selectedRUT}`;
      console.log("Fetching URL:", url);

      const response = await fetch(url);
      console.log("Response status:", response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error response:", errorText);
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Libros prestados recibidos:", data);
      console.log("Cantidad de préstamos:", data.length);

      // Transformar datos para aplanar objetos anidados
      const transformedData = data.map(item => {
        const flat = {
          RUT: item.RUT,
          ISBN: item.ISBN,
          numero: item.numero,
          Fecha_prestamo: item.Fecha_prestamo,
          Fecha_devolucion: item.Fecha_devolucion,
        };
        
        // Aplanar libro
        if (item.libro) {
          flat.libro_titulo = item.libro.titulo;
          flat.libro_autores = Array.isArray(item.libro.autores) 
            ? item.libro.autores.join(', ') 
            : item.libro.autores;
        }
        
        // Aplanar edicion
        if (item.edicion) {
          flat.edicion_ISBN = item.edicion.ISBN;
          flat.edicion_anio = item.edicion.anio;
          flat.edicion_idioma = item.edicion.idioma;
        }
        
        return flat;
      });

      setLibrosPrestados(transformedData);
    } catch (err) {
      console.error("❌ Error consultando libros prestados:", err);
      setLibrosPrestados([]);
      alert("Error al consultar libros prestados: " + err.message);
    } finally {
      setLoadingConsulta2(false);
    }
  };

  return (
    <div className="page">
      <h1>CRUD BIBLIOTECA - MONGODB</h1>
      <div className="img-container">
        <h2>Modelo Entidad Relación</h2>
        <img src={modeloER} />
      </div>
      <NavigationTab selection={selectedTab} setSelection={setSelection} />

      {selectedTab === null ? (
        <div className="table-container">
          <p>Selecciona una entidad para comenzar (Usuario, Autor, Libro, Edición, Copia o Préstamo)</p>
        </div>
      ) : (
        <div className="table-container">
          {loading && <p>Cargando datos...</p>}
          {error && <p style={{ color: "var(--color1)" }}>Error: {error}</p>}

          {!loading && rows.length > 0 && (
            <Table
              rows={rows}
              deleteRow={handleDeleteRow}
              editRow={handleEditRow}
            />
          )}

          {!loading && rows.length === 0 && !error && (
            <p>No hay datos para mostrar</p>
          )}

          <button
            className="btn"
            onClick={() => {
              setModalOpen(true);
              setRowToEdit(null);
            }}
          >
            Agregar Nuevo
          </button>

          {modalOpen && (
            <Modal
              closeModal={() => {
                setModalOpen(false);
                setRowToEdit(null);
              }}
              onSubmit={handleSubmit}
              defaultValue={rowToEdit !== null && rows[rowToEdit]}
              formFields={getFormFields()}
              entityType={selectedTab}
            />
          )}
        </div>
      )}

      {/* ========== SECCIÓN DE CONSULTAS ========== */}
      <div style={{ marginTop: "60px", marginBottom: "60px" }}>
        <h2 style={{ marginBottom: "40px", color: "var(--color4)" }}>
          📊 Consultas Especiales
        </h2>

        {/* CONSULTA 1: Copias con Detalle */}
        <div
          className="table-container"
          style={{
            marginBottom: "40px",
            minHeight: "auto",
            height: "auto",
            padding: "30px",
          }}
        >
          <h3
            style={{
              color: "var(--color4)",
              fontSize: "24px",
              marginBottom: "15px",
              fontFamily: "Arial, Helvetica, sans-serif",
            }}
          >
            📚 CONSULTA 1: Copias de Libros con Detalle
          </h3>
          <p style={{ marginBottom: "20px" }}>
            Muestra un listado completo de todas las copias de libros incluyendo información de AUTOR, LIBRO, EDICIÓN y COPIA
          </p>

          <div
            style={{
              marginBottom: "30px",
              display: "flex",
              gap: "15px",
              alignItems: "center",
              flexWrap: "wrap",
            }}
          >
            <button
              className="btn"
              onClick={consultarCopiasDetalle}
              disabled={loadingConsulta1}
            >
              {loadingConsulta1 ? "Consultando..." : "🔍 Consultar Copias"}
            </button>
          </div>

          {loadingConsulta1 ? (
            <p>Cargando...</p>
          ) : copiasList.length > 0 ? (
            <div className="table-wrapper">
              <p style={{ marginBottom: "15px", fontWeight: "bold" }}>
                📋 Total de copias encontradas: {copiasList.length}
              </p>
              <Table
                rows={copiasList}
                deleteRow={() => {}}
                editRow={() => {}}
              />
            </div>
          ) : (
            <p>
              No hay copias para mostrar. Presiona el botón "Consultar Copias" para ver el listado.
            </p>
          )}
        </div>

        {/* CONSULTA 2: Libros Prestados por Usuario */}
        <div
          className="table-container"
          style={{ minHeight: "auto", height: "auto", padding: "30px" }}
        >
          <h3
            style={{
              color: "var(--color4)",
              fontSize: "24px",
              marginBottom: "15px",
              fontFamily: "Arial, Helvetica, sans-serif",
            }}
          >
            👤 CONSULTA 2: Libros Prestados por Usuario
          </h3>
          <p style={{ marginBottom: "20px" }}>
            Lista todos los libros prestados por un usuario específico, incluyendo detalles del libro, edición y fechas de préstamo
          </p>

          <div
            style={{
              marginBottom: "30px",
              display: "flex",
              gap: "15px",
              alignItems: "center",
              flexWrap: "wrap",
            }}
          >
            <label
              style={{
                color: "var(--color4)",
                fontWeight: "bold",
                fontFamily: "Arial, Helvetica, sans-serif",
              }}
            >
              RUT del Usuario:
            </label>
            <input
              type="text"
              value={selectedRUT}
              onChange={(e) => setSelectedRUT(e.target.value)}
              placeholder="Ej: 12345678-9"
              style={{
                padding: "10px",
                borderRadius: "10px",
                border: "none",
                width: "200px",
                fontFamily: "Arial, Helvetica, sans-serif",
              }}
            />
            <button
              className="btn"
              onClick={consultarLibrosPrestados}
              disabled={loadingConsulta2}
            >
              {loadingConsulta2 ? "Consultando..." : "🔍 Consultar Préstamos"}
            </button>
          </div>

          {loadingConsulta2 ? (
            <p>Cargando...</p>
          ) : librosPrestados.length > 0 ? (
            <div className="table-wrapper">
              <p style={{ marginBottom: "15px", fontWeight: "bold" }}>
                📋 Total de préstamos encontrados: {librosPrestados.length}
              </p>
              <Table
                rows={librosPrestados}
                deleteRow={() => {}}
                editRow={() => {}}
              />
            </div>
          ) : (
            <p>
              No hay préstamos para mostrar. Ingresa un RUT y presiona "Consultar Préstamos".
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;