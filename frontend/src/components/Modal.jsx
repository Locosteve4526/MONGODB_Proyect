import React, { useState } from "react";

import "./Modal.css";

export const Modal = ({
  closeModal,
  onSubmit,
  defaultValue,
  formFields,
  entityType,
}) => {
  const [formState, setFormState] = useState(
    defaultValue || Object.fromEntries(formFields.map((field) => [field, ""]))
  );

  const [errors, setErrors] = useState("");

  const validateForm = () => {
    // Validar que todos los campos tengan valores no vacíos
    const hasEmptyFields = Object.values(formState).some((value) => {
      if (value === null || value === undefined) return true;
      if (typeof value === "string" && value.trim() === "") return true;
      return false;
    });

    if (!hasEmptyFields) {
      setErrors("");
      return true;
    } else {
      let errorFields = [];
      for (const [key, value] of Object.entries(formState)) {
        if (!value || (typeof value === "string" && value.trim() === "")) {
          errorFields.push(key);
        }
      }

      setErrors(errorFields.join(", "));
      return false;
    }
  };

  const handleChange = (e) => {
    setFormState({
      ...formState,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    console.log("=== MODAL SUBMIT ===");
    console.log("📋 Form State Original:", formState);
    console.log("🏷️ Entity Type:", entityType);

    // Limpiar y transformar los datos según la entidad
    const cleanedData = {};

    for (const [key, value] of Object.entries(formState)) {
      let fieldName = key;
      // Procesar según el tipo de campo y entidad
      if (key === "RUT" && (entityType === 1 || entityType === 6)) {
        cleanedData[fieldName] = value ? parseInt(value, 10) : "";
        console.log(
          `🔢 Convirtiendo ${fieldName} a número:`,
          cleanedData[fieldName]
        );
      } else if (key === "numero" && (entityType === 5 || entityType === 6)) {
        // Número de copia - debe ser número entero
        cleanedData[fieldName] = value ? parseInt(value, 10) : "";
        console.log(
          `🔢 Convirtiendo ${fieldName} a número:`,
          cleanedData[fieldName]
        );
      } else if (key === "anio" && entityType === 4) {
        // Año de edición - debe ser número entero
        cleanedData[fieldName] = value ? parseInt(value, 10) : "";
        console.log(
          `🔢 Convirtiendo ${fieldName} a número:`,
          cleanedData[fieldName]
        );
      } else if (key === "autores" && entityType === 3) {
        // Autores de libro - debe ser array
        const authorsArray = value
          ? value
              .split(",")
              .map((author) => author.trim())
              .filter((a) => a)
          : [];
        cleanedData[fieldName] = authorsArray;
        console.log(
          `📚 Convirtiendo ${fieldName} a array:`,
          cleanedData[fieldName]
        );
      } else {
        // Otros campos se envían como string limpio
        cleanedData[fieldName] =
          typeof value === "string" ? value.trim() : value;
        console.log(`✏️ Campo ${fieldName}:`, cleanedData[fieldName]);
      }
    }

    console.log("✅ Datos limpiados a enviar:", cleanedData);
    console.log("📤 JSON final:", JSON.stringify(cleanedData, null, 2));

    onSubmit(cleanedData);

    closeModal();
  };

  // Función para determinar el tipo de input
  const getInputType = (field) => {
    if (
      field === "fechorCom" ||
      field === "fechorAut" ||
      field === "fecha_prestamo" ||
      field === "fecha_devolucion"
    ) {
      return "date";
    }
    if (field === "anio" || field === "numero") {
      return "number";
    }
    return "text";
  };

  // Función para obtener placeholder apropiado
  const getPlaceholder = (field, entityType) => {
    if (field === "RUT") return "Ej: 12345678-9";
    if (field === "nombre" && entityType === 1) return "Nombre del usuario";
    if (field === "nombre" && entityType === 2) return "Nombre del autor";
    if (field === "titulo") return "Título del libro";
    if (field === "autores") return "Autor1, Autor2, Autor3...";
    if (field === "ISBN") return "Ej: 978-3-16-148410-0";
    if (field === "anio") return "Ej: 2023";
    if (field === "idioma") return "Ej: Español";
    if (field === "numero") return "Número de copia";
    if (field === "fecha_prestamo") return "Fecha de préstamo";
    if (field === "fecha_devolucion") return "Fecha de devolución";
    return "";
  };

  return (
    <div
      className="modal-container"
      onClick={(e) => {
        if (e.target.className === "modal-container") {
          closeModal();
        }
      }}
    >
      <div className="modal">
        <form>
          {formFields.map((field) => {
            return (
              <div key={field} className="form-group">
                <label htmlFor={field}>{field}</label>

                {/* Select especial para likeNotLike */}
                {field === "likeNotLike" ? (
                  <select
                    name={field}
                    value={formState[field] || ""}
                    onChange={handleChange}
                    style={{
                      padding: "10px",
                      borderRadius: "10px",
                      border: "1px solid #ddd",
                      width: "100%",
                      fontFamily: "Arial, Helvetica, sans-serif",
                      fontSize: "14px",
                    }}
                  >
                    <option value="">Selecciona una opción...</option>
                    <option value="megusta">👍 Me gusta</option>
                    <option value="nomegusta">👎 No me gusta</option>
                  </select>
                ) : (
                  <input
                    type={getInputType(field)}
                    name={field}
                    value={formState[field] || ""}
                    onChange={handleChange}
                    placeholder={getPlaceholder(field, entityType)}
                    style={{
                      fontFamily: "Arial, Helvetica, sans-serif",
                    }}
                  />
                )}
              </div>
            );
          })}
          {errors && <div className="error">{"Complete: " + errors}</div>}
          <button type="submit" className="btn" onClick={handleSubmit}>
            Guardar
          </button>
        </form>
      </div>
    </div>
  );
};
