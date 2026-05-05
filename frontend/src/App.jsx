import { useState } from "react";
import UploadArea from "./components/UploadArea";
import InvoiceSummary from "./components/InvoiceSummary";
import InvoiceTable from "./components/InvoiceTable";
import InvoiceHistory from "./components/InvoiceHistory";

export default function App() {
  const [invoiceData, setInvoiceData] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleResult = (data) => {
    setInvoiceData(data);
  };

  const handleUploadComplete = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-gray-800 bg-black/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Analizador de Facturas</h1>
              <p className="text-sm text-gray-400 mt-1">Análisis inteligente de facturas con IA</p>
            </div>
            <div className="text-sm text-gray-500">
              Sesión: {Math.random().toString(36).substring(7).toUpperCase()}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar - History */}
          <aside className="lg:col-span-1">
            <div className="sticky top-24 bg-gray-950 border border-gray-800 rounded-lg p-6 shadow-lg">
              <h2 className="text-lg font-semibold mb-4">Historial de Facturas</h2>
              <InvoiceHistory key={refreshKey} onSelect={handleResult} />
            </div>
          </aside>

          {/* Main Panel */}
          <section className="lg:col-span-3 space-y-6">
            {/* Upload Section */}
            <div className="bg-gray-950 border border-gray-800 rounded-lg p-8 shadow-lg">
              <h2 className="text-xl font-semibold mb-6">Subir Factura</h2>
              <UploadArea onResult={handleResult} onUploadComplete={handleUploadComplete} />
            </div>

            {/* Invoice Details */}
            {invoiceData && (
              <>
                <div className="bg-gray-950 border border-gray-800 rounded-lg p-8 shadow-lg">
                  <h2 className="text-xl font-semibold mb-6">Detalles de la Factura</h2>
                  <InvoiceSummary invoice={invoiceData} />
                </div>

                {/* Items Table */}
                <div className="bg-gray-950 border border-gray-800 rounded-lg p-8 shadow-lg">
                  <h2 className="text-xl font-semibold mb-6">Artículos</h2>
                  <InvoiceTable items={invoiceData.items} subtotal={invoiceData.total} />
                </div>
              </>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}
