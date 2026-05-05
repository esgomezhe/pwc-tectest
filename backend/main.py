import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from crud import get_invoice_by_id, get_invoices_by_session, save_invoice
from data_processor import process_invoice_data
from database import Base, engine, get_db
from llm_service import analyze_invoice
from models import Invoice, InvoiceItem
from pdf_extractor import extract_text_from_pdf
from schemas import InvoiceListItem, InvoiceOut

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Invoice Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN")],
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

    return invoice


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
    return invoice
