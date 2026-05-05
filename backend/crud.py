from sqlalchemy.orm import Session

from models import Invoice, InvoiceItem


def save_invoice(db: Session, session_id: str, filename: str, invoice_dict: dict) -> Invoice:
    invoice = Invoice(
        session_id=session_id,
        nombre_archivo=filename,
        tipo_documento=invoice_dict.get("tipo_documento"),
        numero_factura=invoice_dict.get("numero_factura"),
        fecha_emision=invoice_dict.get("fecha_emision"),
        fecha_vencimiento=invoice_dict.get("fecha_vencimiento"),
        emisor_nombre=invoice_dict.get("emisor_nombre"),
        emisor_nit=invoice_dict.get("emisor_nit"),
        emisor_direccion=invoice_dict.get("emisor_direccion"),
        emisor_ciudad=invoice_dict.get("emisor_ciudad"),
        emisor_telefono=invoice_dict.get("emisor_telefono"),
        cliente_nombre=invoice_dict.get("cliente_nombre"),
        cliente_documento=invoice_dict.get("cliente_documento"),
        cliente_direccion=invoice_dict.get("cliente_direccion"),
        cliente_ciudad=invoice_dict.get("cliente_ciudad"),
        cliente_telefono=invoice_dict.get("cliente_telefono"),
        cliente_email=invoice_dict.get("cliente_email"),
        condicion_pago=invoice_dict.get("condicion_pago"),
        medio_pago=invoice_dict.get("medio_pago"),
        moneda=invoice_dict.get("moneda"),
        subtotal=invoice_dict.get("subtotal"),
        descuento=invoice_dict.get("descuento"),
        impuestos=invoice_dict.get("impuestos"),
        total=invoice_dict.get("total"),
        cufe=invoice_dict.get("cufe"),
        resolucion_dian=invoice_dict.get("resolucion_dian"),
        notas=invoice_dict.get("notas"),
        resumen=invoice_dict.get("resumen"),
    )
    db.add(invoice)
    db.flush()

    for item in invoice_dict.get("items", []):
        db_item = InvoiceItem(
            invoice_id=invoice.id,
            codigo=item.get("codigo"),
            descripcion=item.get("descripcion"),
            cantidad=item.get("cantidad"),
            unidad_medida=item.get("unidad_medida"),
            precio_unitario=item.get("precio_unitario"),
            descuento=item.get("descuento"),
            subtotal=item.get("subtotal"),
        )
        db.add(db_item)

    db.commit()
    db.refresh(invoice)
    return invoice


def get_invoices_by_session(db: Session, session_id: str) -> list[Invoice]:
    return (
        db.query(Invoice)
        .filter(Invoice.session_id == session_id)
        .order_by(Invoice.created_at.desc())
        .all()
    )


def get_invoice_by_id(db: Session, invoice_id: int, session_id: str) -> Invoice | None:
    return (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id, Invoice.session_id == session_id)
        .first()
    )
