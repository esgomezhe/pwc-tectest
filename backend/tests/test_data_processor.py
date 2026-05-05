import json
import os

from data_processor import process_invoice_data

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def load_previous_output(filename):
    with open(os.path.join(OUTPUT_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


def test_process_factura_seven():
    previous = load_previous_output("llm_analysis.json")
    data = previous["resultado"].copy()

    result = process_invoice_data(data)
    stats = result["estadisticas"]

    assert stats["cantidad_items"] == 2
    assert stats["cantidad_unidades"] == 2
    assert stats["item_mas_costoso"] == "JEAN CARGO TONO MEDIO OSCURO"
    assert stats["item_mas_barato"] == "VARIOS BOLSA SEVEN TELA MEDIANA NEGRA 40X36CM"
    assert stats["precio_promedio"] == 75798.0
    assert stats["total_descuentos"] == 90705.88
    assert stats["porcentaje_descuento"] > 0
    assert stats["subtotal_calculado"] == 60891.0
    assert stats["valor_bruto_total"] == 151596.0
    assert "JEAN CARGO TONO MEDIO OSCURO" in stats["distribucion_precio"]

    output = {
        "archivo": previous["archivo"],
        "etapa": "procesamiento_pandas",
        "estadisticas": stats,
        "items_enriquecidos": result["items"],
    }
    with open(os.path.join(OUTPUT_DIR, "pandas_analysis.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
