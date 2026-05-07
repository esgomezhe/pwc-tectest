export default function InvoiceTable({ items, subtotal }) {
  if (!items || items.length === 0) {
    return <p className="text-gray-400 text-center py-4">Sin artículos</p>;
  }

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("es-CO", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value || 0);
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b-2 border-gray-800">
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase tracking-wide">
              Descripción
            </th>
            <th className="px-4 py-3 text-right text-xs font-semibold text-gray-400 uppercase tracking-wide">
              Cant.
            </th>
            <th className="px-4 py-3 text-right text-xs font-semibold text-gray-400 uppercase tracking-wide">
              P. Unitario
            </th>
            <th className="px-4 py-3 text-right text-xs font-semibold text-gray-400 uppercase tracking-wide">
              Descuento
            </th>
            <th className="px-4 py-3 text-right text-xs font-semibold text-gray-400 uppercase tracking-wide">
              Subtotal
            </th>
            <th className="px-4 py-3 text-right text-xs font-semibold text-gray-400 uppercase tracking-wide">
              Participación
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800">
          {items.map((item, idx) => (
            <tr key={idx} className="hover:bg-gray-900/50 transition">
              <td className="px-4 py-3 text-white">{item.descripcion}</td>
              <td className="px-4 py-3 text-right text-white font-semibold">
                {item.cantidad}
              </td>
              <td className="px-4 py-3 text-right text-gray-300">
                ${formatCurrency(item.precio_unitario)}
              </td>
              <td className="px-4 py-3 text-right text-red-400 font-semibold">
                {item.descuento > 0
                  ? `-$${formatCurrency(item.descuento)} (${item.descuento_porcentual}%)`
                  : "—"}
              </td>
              <td className="px-4 py-3 text-right text-white font-bold">
                ${formatCurrency(item.subtotal)}
              </td>
              <td className="px-4 py-3 text-right text-blue-400 font-semibold">
                {item.participacion != null ? `${item.participacion}%` : "—"}
              </td>
            </tr>
          ))}
          <tr className="bg-gray-900/50 border-t-2 border-gray-700">
            <td colSpan="5" className="px-4 py-4 text-right font-semibold text-gray-300">
              Total:
            </td>
            <td className="px-4 py-4 text-right font-bold text-lg text-blue-400">
              ${formatCurrency(subtotal)}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
