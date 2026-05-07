from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InvoiceItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str | None = None
    descripcion: str | None = None
    cantidad: float | None = None
    unidad_medida: str | None = None
    precio_unitario: float | None = None
    descuento: float | None = None
    subtotal: float | None = None
    valor_bruto: float | None = None
    descuento_porcentual: float | None = None
    participacion: float | None = None


class EstadisticasOut(BaseModel):
    cantidad_items: int = 0
    cantidad_unidades: int = 0
    item_mas_costoso: str | None = None
    item_mas_barato: str | None = None
    precio_promedio: float = 0
    precio_mediana: float = 0
    precio_maximo: float = 0
    precio_minimo: float = 0
    desviacion_estandar: float = 0
    total_descuentos: float = 0
    porcentaje_descuento: float = 0
    subtotal_calculado: float = 0
    valor_bruto_total: float = 0
    distribucion_precio: dict[str, float] = {}


class InvoiceOut(BaseModel):
    id: int
    session_id: str
    nombre_archivo: str

    tipo_documento: str | None = None
    numero_factura: str | None = None
    fecha_emision: str | None = None
    fecha_vencimiento: str | None = None

    emisor_nombre: str | None = None
    emisor_nit: str | None = None
    emisor_direccion: str | None = None
    emisor_ciudad: str | None = None
    emisor_telefono: str | None = None

    cliente_nombre: str | None = None
    cliente_documento: str | None = None
    cliente_direccion: str | None = None
    cliente_ciudad: str | None = None
    cliente_telefono: str | None = None
    cliente_email: str | None = None

    condicion_pago: str | None = None
    medio_pago: str | None = None
    moneda: str | None = None

    subtotal: float | None = None
    descuento: float | None = None
    impuestos: float | None = None
    total: float | None = None

    cufe: str | None = None
    resolucion_dian: str | None = None
    notas: str | None = None
    resumen: str | None = None

    created_at: datetime
    items: list[InvoiceItemOut]
    estadisticas: EstadisticasOut | None = None


class InvoiceListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre_archivo: str
    tipo_documento: str | None = None
    emisor_nombre: str | None = None
    numero_factura: str | None = None
    total: float | None = None
    moneda: str | None = None
    created_at: datetime
