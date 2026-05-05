import fitz
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
import models
from main import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Base.metadata.create_all(bind=engine)
TestSession = sessionmaker(bind=engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_health_check():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_analyze_rejects_non_pdf():
    r = client.post(
        "/analyze",
        headers={"X-Session-ID": "test-123"},
        files={"file": ("archivo.txt", b"contenido", "text/plain")},
    )
    assert r.status_code == 400
    assert "PDF" in r.json()["detail"]


def test_analyze_rejects_empty_pdf():
    doc = fitz.open()
    doc.new_page()
    pdf_bytes = doc.tobytes()
    doc.close()

    r = client.post(
        "/analyze",
        headers={"X-Session-ID": "test-123"},
        files={"file": ("vacio.pdf", pdf_bytes, "application/pdf")},
    )
    assert r.status_code == 422
    assert "texto" in r.json()["detail"].lower()


def test_analyze_requires_session_header():
    r = client.post("/analyze", files={"file": ("test.pdf", b"fake", "application/pdf")})
    assert r.status_code == 422


def test_invoices_empty_session():
    r = client.get("/invoices", headers={"X-Session-ID": "no-existe"})
    assert r.status_code == 200
    assert r.json() == []


def test_invoice_not_found():
    r = client.get("/invoices/999", headers={"X-Session-ID": "test-123"})
    assert r.status_code == 404
