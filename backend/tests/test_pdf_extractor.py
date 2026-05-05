import json
import os

from pdf_extractor import extract_text_from_pdf

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "examples")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def read_pdf(filename):
    with open(os.path.join(EXAMPLES_DIR, filename), "rb") as f:
        return f.read()


def test_extract_factura_seven():
    text = extract_text_from_pdf(read_pdf("ad086050315901026178684401.pdf"))

    assert "PASH S.A.S" in text
    assert "615822450" in text
    assert "JEAN CARGO" in text

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output = {
        "archivo": "ad086050315901026178684401.pdf",
        "etapa": "extraccion_texto",
        "caracteres": len(text),
        "texto_extraido": text,
    }
    with open(os.path.join(OUTPUT_DIR, "pdf_extraction.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
