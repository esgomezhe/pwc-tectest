import { useState } from "react";
import axios from "axios";
import { getSessionId } from "../utils/sessionUtils";

export default function UploadArea({ onResult, onUploadComplete }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      processFile(files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files.length > 0) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = async (file) => {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Solo se soportan archivos PDF");
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post("http://localhost:8000/analyze", formData, {
        headers: {
          "X-Session-ID": getSessionId(),
          "Content-Type": "multipart/form-data",
        },
      });

      onResult(response.data);
      onUploadComplete();
    } catch (err) {
      setError(err.response?.data?.detail || "Error procesando el PDF");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      <div
        onDrop={handleDrop}
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        className={`border-2 border-dashed rounded-lg p-12 text-center transition-all duration-200 ${
          dragActive
            ? "border-blue-500 bg-blue-500/10"
            : "border-gray-700 bg-gray-900 hover:border-gray-600"
        }`}
      >
        {!loading ? (
          <>
            <p className="text-lg font-semibold mb-2">Arrastra tu PDF aquí</p>
            <p className="text-sm text-gray-400 mb-6">o haz clic para explorar</p>
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileInput}
              className="hidden"
              id="pdf-input"
            />
            <label htmlFor="pdf-input">
              <button
                type="button"
                onClick={() => document.getElementById("pdf-input").click()}
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200"
              >
                Seleccionar PDF
              </button>
            </label>
          </>
        ) : (
          <>
            <div className="flex justify-center mb-4">
              <div className="animate-spin rounded-full h-12 w-12 border-2 border-blue-600 border-t-transparent"></div>
            </div>
            <p className="font-semibold">Analizando factura...</p>
            <p className="text-sm text-gray-400 mt-1">Esto puede tomar un momento</p>
          </>
        )}
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-900/20 border border-red-700 text-red-300 rounded-lg">
          {error}
        </div>
      )}
    </div>
  );
}
