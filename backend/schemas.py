from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InvoiceItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str | None
    descripcion: str | None
    cantidad: float | None
    unidad_medida: str | None
    precio_unitario: float | None
    descuento: float | None
    subtotal: float | None


class InvoiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: str
    nombre_archivo: str

    tipo_documento: str | None
    numero_factura: str | None
    fecha_emision: str | None
    fecha_vencimiento: str | None

    emisor_nombre: str | None
    emisor_nit: str | None
    emisor_direccion: str | None
    emisor_ciudad: str | None
    emisor_telefono: str | None

    cliente_nombre: str | None
    cliente_documento: str | None
    cliente_direccion: str | None
    cliente_ciudad: str | None
    cliente_telefono: str | None
    cliente_email: str | None

    condicion_pago: str | None
    medio_pago: str | None
    moneda: str | None

    subtotal: float | None
    descuento: float | None
    impuestos: float | None
    total: float | None

    cufe: str | None
    resolucion_dian: str | None
    notas: str | None
    resumen: str | None

    created_at: datetime
    items: list[InvoiceItemOut]


class InvoiceListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre_archivo: str
    tipo_documento: str | None
    emisor_nombre: str | None
    numero_factura: str | None
    total: float | None
    moneda: str | None
    created_at: datetime
