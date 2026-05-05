import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.crud import save_invoice, get_invoices_by_session, get_invoice_by_id

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def load_previous_output(filename):
    with open(os.path.join(OUTPUT_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


def get_test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_save_factura_seven():
    db = get_test_db()
    previous = load_previous_output("llm_analysis.json")
    data = previous["resultado"]

    invoice = save_invoice(db, "session-test", "factura_seven.pdf", data)

    assert invoice.id is not None
    assert invoice.emisor_nombre == "PASH S.A.S"
    assert invoice.total == 72460.0
    assert len(invoice.items) == 2
    assert invoice.items[0].descripcion == "JEAN CARGO TONO MEDIO OSCURO"


def test_get_invoices_by_session():
    db = get_test_db()
    previous = load_previous_output("llm_analysis.json")
    data = previous["resultado"]

    save_invoice(db, "session-1", "factura1.pdf", data)
    save_invoice(db, "session-1", "factura2.pdf", data)

    result = get_invoices_by_session(db, "session-1")
    assert len(result) == 2


def test_get_invoice_by_id_validates_session():
    db = get_test_db()
    previous = load_previous_output("llm_analysis.json")
    data = previous["resultado"]

    invoice = save_invoice(db, "session-1", "factura.pdf", data)

    found = get_invoice_by_id(db, invoice.id, "session-1")
    assert found is not None
    assert found.emisor_nombre == "PASH S.A.S"

    not_found = get_invoice_by_id(db, invoice.id, "session-otro")
    assert not_found is None
