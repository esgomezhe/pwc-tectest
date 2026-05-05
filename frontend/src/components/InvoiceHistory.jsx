import { useEffect, useState } from "react";
import axios from "axios";
import { getSessionId } from "../utils/sessionUtils";

export default function InvoiceHistory({ onSelect }) {
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchInvoices = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:8000/invoices", {
        headers: { "X-Session-ID": getSessionId() },
      });
      setInvoices(response.data);
    } catch (err) {
      console.error("Error al obtener facturas", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInvoices();
  }, []);

  const handleSelectInvoice = async (id) => {
    try {
      const response = await axios.get(`http://localhost:8000/invoices/${id}`, {
        headers: { "X-Session-ID": getSessionId() },
      });
      onSelect(response.data);
    } catch (err) {
      console.error("Error al obtener factura", err);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("es-CO", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value || 0);
  };

  if (loading && invoices.length === 0) {
    return <div className="text-center text-gray-400 py-4">Cargando...</div>;
  }

  if (invoices.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-400 text-sm">Sin facturas aún</p>
        <p className="text-gray-500 text-xs mt-2">Sube una para comenzar</p>
      </div>
    );
  }

  return (
    <div>
      <button
        onClick={fetchInvoices}
        className="w-full bg-gray-800 hover:bg-gray-700 text-white py-2 px-3 rounded-lg text-sm font-semibold transition-colors duration-200 mb-4"
      >
        Actualizar
      </button>
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {invoices.map((invoice) => (
          <button
            key={invoice.id}
            onClick={() => handleSelectInvoice(invoice.id)}
            className="w-full text-left p-4 bg-gray-900 border border-gray-800 rounded-lg hover:border-blue-600 hover:bg-gray-800 transition-all duration-200 text-sm"
          >
            <p className="font-semibold text-white truncate">
              {invoice.emisor_nombre}
            </p>
            <p className="text-xs text-gray-400 mt-1 truncate">
              {invoice.nombre_archivo}
            </p>
            <div className="flex items-center justify-between mt-2">
              <p className="text-sm font-bold text-blue-400">
                ${formatCurrency(invoice.total)}
              </p>
              <p className="text-xs text-gray-500">
                {new Date(invoice.created_at).toLocaleDateString("es-CO")}
              </p>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
