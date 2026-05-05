import json
import os

import pytest

from app.services.llm_service import analyze_invoice

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def load_previous_output(filename):
    with open(os.path.join(OUTPUT_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.integration
def test_analyze_factura_seven():
    previous = load_previous_output("pdf_extraction.json")
    text = previous["texto_extraido"]

    result = analyze_invoice(text)

    assert result["emisor_nombre"] is not None
    assert "PASH" in result["emisor_nombre"].upper() or "SEVEN" in result["emisor_nombre"].upper()
    assert result["total"] == pytest.approx(72460.0, rel=0.01)
    assert result["moneda"] == "COP"
    assert len(result["items"]) == 2

    output = {
        "archivo": previous["archivo"],
        "etapa": "analisis_llm",
        "modelo": "gemini-2.5-flash",
        "resultado": result,
    }
    with open(os.path.join(OUTPUT_DIR, "llm_analysis.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
