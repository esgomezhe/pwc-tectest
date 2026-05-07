import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.crud import get_invoice_by_id, get_invoices_by_session, save_invoice
from app.database import Base, engine, get_db
from app.models import Invoice
from app.schemas import InvoiceListItem, InvoiceOut
from app.services.data_processor import process_invoice_data
from app.services.llm_service import analyze_invoice
from app.services.pdf_extractor import extract_text_from_pdf

load_dotenv()

Base.metadata.create_all(bind=engine)


def build_invoice_response(invoice: Invoice) -> dict:
    items_data = [
        {
            "id": item.id,
            "codigo": item.codigo,
            "descripcion": item.descripcion,
            "cantidad": item.cantidad,
            "unidad_medida": item.unidad_medida,
            "precio_unitario": item.precio_unitario,
            "descuento": item.descuento,
            "subtotal": item.subtotal,
        }
        for item in invoice.items
    ]

    enriched = process_invoice_data({"items": items_data})

    response = {
        "id": invoice.id,
        "session_id": invoice.session_id,
        "nombre_archivo": invoice.nombre_archivo,
        "tipo_documento": invoice.tipo_documento,
        "numero_factura": invoice.numero_factura,
        "fecha_emision": invoice.fecha_emision,
        "fecha_vencimiento": invoice.fecha_vencimiento,
        "emisor_nombre": invoice.emisor_nombre,
        "emisor_nit": invoice.emisor_nit,
        "emisor_direccion": invoice.emisor_direccion,
        "emisor_ciudad": invoice.emisor_ciudad,
        "emisor_telefono": invoice.emisor_telefono,
        "cliente_nombre": invoice.cliente_nombre,
        "cliente_documento": invoice.cliente_documento,
        "cliente_direccion": invoice.cliente_direccion,
        "cliente_ciudad": invoice.cliente_ciudad,
        "cliente_telefono": invoice.cliente_telefono,
        "cliente_email": invoice.cliente_email,
        "condicion_pago": invoice.condicion_pago,
        "medio_pago": invoice.medio_pago,
        "moneda": invoice.moneda,
        "subtotal": invoice.subtotal,
        "descuento": invoice.descuento,
        "impuestos": invoice.impuestos,
        "total": invoice.total,
        "cufe": invoice.cufe,
        "resolucion_dian": invoice.resolucion_dian,
        "notas": invoice.notas,
        "resumen": invoice.resumen,
        "created_at": invoice.created_at,
        "items": enriched["items"],
        "estadisticas": enriched.get("estadisticas"),
    }

    return response

app = FastAPI(title="Invoice Analyzer", version="1.0.0")

cors_origins = [
    os.getenv("CORS_ORIGIN")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Invoice Analyzer"}


@app.post("/analyze", response_model=InvoiceOut)
def analyze_pdf(
    file: UploadFile = File(...),
    x_session_id: str = Header(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    file_bytes = file.file.read()
    text = extract_text_from_pdf(file_bytes)

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No se pudo extraer texto del PDF. Puede ser un documento escaneado sin OCR.",
        )

    try:
        invoice_dict = analyze_invoice(text)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            raise HTTPException(
                status_code=429,
                detail="Cuota de Gemini API agotada. Intenta de nuevo en unos minutos.",
            )
        raise HTTPException(status_code=502, detail="Error al comunicarse con el servicio de IA.")

    invoice_dict = process_invoice_data(invoice_dict)
    invoice = save_invoice(db, x_session_id, file.filename, invoice_dict)

    return build_invoice_response(invoice)


@app.get("/invoices", response_model=list[InvoiceListItem])
def list_invoices(
    x_session_id: str = Header(...),
    db: Session = Depends(get_db),
):
    return get_invoices_by_session(db, x_session_id)


@app.get("/invoices/{invoice_id}", response_model=InvoiceOut)
def get_invoice(
    invoice_id: int,
    x_session_id: str = Header(...),
    db: Session = Depends(get_db),
):
    invoice = get_invoice_by_id(db, invoice_id, x_session_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return build_invoice_response(invoice)
