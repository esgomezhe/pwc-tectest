export default function InvoiceStats({ estadisticas }) {
  if (!estadisticas || estadisticas.cantidad_items === 0) {
    return null;
  }

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("es-CO", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value || 0);
  };

  const formatPercent = (value) => {
    return `${(value || 0).toFixed(1)}%`;
  };

  return (
    <div className="space-y-4">
      {/* Key Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
            Artículos
          </p>
          <p className="text-white font-bold text-lg mt-2">
            {estadisticas.cantidad_items}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            {estadisticas.cantidad_unidades} unidades
          </p>
        </div>
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
            Precio Promedio
          </p>
          <p className="text-white font-bold text-lg mt-2">
            ${formatCurrency(estadisticas.precio_promedio)}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Mediana: ${formatCurrency(estadisticas.precio_mediana)}
          </p>
        </div>
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
            Desviación Estándar
          </p>
          <p className="text-white font-bold text-lg mt-2">
            ${formatCurrency(estadisticas.desviacion_estandar)}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Variabilidad de precios
          </p>
        </div>
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
            Descuentos
          </p>
          <p className="text-red-400 font-bold text-lg mt-2">
            ${formatCurrency(estadisticas.total_descuentos)}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            {formatPercent(estadisticas.porcentaje_descuento)} del bruto
          </p>
        </div>
      </div>

      {/* Price Range */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
            Más Costoso
          </p>
          <p className="text-white font-semibold mt-2 truncate">
            {estadisticas.item_mas_costoso}
          </p>
          <p className="text-sm text-blue-400 font-bold mt-1">
            ${formatCurrency(estadisticas.precio_maximo)}
          </p>
        </div>
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
            Más Barato
          </p>
          <p className="text-white font-semibold mt-2 truncate">
            {estadisticas.item_mas_barato}
          </p>
          <p className="text-sm text-blue-400 font-bold mt-1">
            ${formatCurrency(estadisticas.precio_minimo)}
          </p>
        </div>
      </div>

      {/* Distribution */}
      {estadisticas.distribucion_precio &&
        Object.keys(estadisticas.distribucion_precio).length > 0 && (
          <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
              Distribución por Artículo
            </p>
            <div className="space-y-2">
              {Object.entries(estadisticas.distribucion_precio).map(
                ([nombre, porcentaje]) => (
                  <div key={nombre}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-300 truncate mr-4">
                        {nombre}
                      </span>
                      <span className="text-white font-semibold">
                        {formatPercent(porcentaje)}
                      </span>
                    </div>
                    <div className="w-full bg-gray-800 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all"
                        style={{ width: `${Math.min(porcentaje, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                )
              )}
            </div>
          </div>
        )}

      {/* Totals Summary */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
            Valor Bruto Total
          </p>
          <p className="text-white font-bold text-lg mt-2">
            ${formatCurrency(estadisticas.valor_bruto_total)}
          </p>
        </div>
        <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
            Subtotal Calculado
          </p>
          <p className="text-white font-bold text-lg mt-2">
            ${formatCurrency(estadisticas.subtotal_calculado)}
          </p>
        </div>
      </div>
    </div>
  );
}
