export default function InvoiceSummary({ invoice }) {
  if (!invoice) {
    return (
      <div className="text-center text-gray-400 py-8">
        Selecciona una factura para ver detalles
      </div>
    );
  }

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("es-CO", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value || 0);
  };

  return (
    <div className="space-y-4">
      {/* Metadata Grid */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Tipo</p>
          <p className="text-white font-semibold mt-2 capitalize">{invoice.tipo_documento}</p>
        </div>
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Factura #</p>
          <p className="text-white font-semibold mt-2">{invoice.numero_factura}</p>
        </div>
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Emitida</p>
          <p className="text-white font-semibold mt-2">{invoice.fecha_emision}</p>
        </div>
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Vence</p>
          <p className="text-white font-semibold mt-2">{invoice.fecha_vencimiento || "—"}</p>
        </div>
      </div>

      {/* Issuer */}
      <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Emisor</p>
        <p className="text-white font-semibold">{invoice.emisor_nombre}</p>
        <p className="text-sm text-gray-400 mt-1">{invoice.emisor_nit}</p>
        {invoice.emisor_direccion && (
          <p className="text-sm text-gray-400">{invoice.emisor_direccion}</p>
        )}
      </div>

      {/* Client */}
      <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Cliente</p>
        <p className="text-white font-semibold">{invoice.cliente_nombre}</p>
        <p className="text-sm text-gray-400 mt-1">{invoice.cliente_documento}</p>
        {invoice.cliente_email && (
          <p className="text-sm text-gray-400">{invoice.cliente_email}</p>
        )}
      </div>

      {/* Amounts */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Subtotal</p>
          <p className="text-white font-bold text-lg mt-2">
            ${formatCurrency(invoice.subtotal)} {invoice.moneda}
          </p>
        </div>
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Descuento</p>
          <p className="text-red-400 font-bold text-lg mt-2">
            -${formatCurrency(invoice.descuento)}
          </p>
        </div>
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Impuestos</p>
          <p className="text-white font-bold text-lg mt-2">
            ${formatCurrency(invoice.impuestos)}
          </p>
        </div>
        <div className="bg-blue-900/30 border border-blue-600 p-4 rounded-lg">
          <p className="text-xs font-semibold text-blue-300 uppercase tracking-wide">Total</p>
          <p className="text-white font-bold text-xl mt-2">
            ${formatCurrency(invoice.total)}
          </p>
        </div>
      </div>

      {/* Summary */}
      <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Resumen</p>
        <p className="text-gray-300 text-sm leading-relaxed">{invoice.resumen}</p>
      </div>

      {/* CUFE if present */}
      {invoice.cufe && (
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">CUFE</p>
          <p className="font-mono text-xs text-gray-500 break-all">{invoice.cufe}</p>
        </div>
      )}
    </div>
  );
}
