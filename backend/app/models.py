from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    nombre_archivo = Column(String, nullable=False)

    tipo_documento = Column(String)
    numero_factura = Column(String)
    fecha_emision = Column(String)
    fecha_vencimiento = Column(String)

    emisor_nombre = Column(String)
    emisor_nit = Column(String)
    emisor_direccion = Column(String)
    emisor_ciudad = Column(String)
    emisor_telefono = Column(String)

    cliente_nombre = Column(String)
    cliente_documento = Column(String)
    cliente_direccion = Column(String)
    cliente_ciudad = Column(String)
    cliente_telefono = Column(String)
    cliente_email = Column(String)

    condicion_pago = Column(String)
    medio_pago = Column(String)
    moneda = Column(String)

    subtotal = Column(Float)
    descuento = Column(Float)
    impuestos = Column(Float)
    total = Column(Float)

    cufe = Column(String)
    resolucion_dian = Column(String)
    notas = Column(String)
    resumen = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("InvoiceItem", back_populates="invoice")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    codigo = Column(String)
    descripcion = Column(String)
    cantidad = Column(Float)
    unidad_medida = Column(String)
    precio_unitario = Column(Float)
    descuento = Column(Float)
    subtotal = Column(Float)

    invoice = relationship("Invoice", back_populates="items")
