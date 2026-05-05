import pandas as pd


def process_invoice_data(invoice_dict: dict) -> dict:
    items = invoice_dict.get("items", [])
    if not items:
        invoice_dict["estadisticas"] = {
            "cantidad_items": 0,
            "item_mas_costoso": None,
            "precio_promedio": 0,
        }
        return invoice_dict

    df = pd.DataFrame(items)

    df["cantidad"] = pd.to_numeric(df.get("cantidad"), errors="coerce").fillna(0)
    df["precio_unitario"] = pd.to_numeric(df.get("precio_unitario"), errors="coerce").fillna(0)
    df["subtotal"] = pd.to_numeric(df.get("subtotal"), errors="coerce").fillna(0)
    df["descuento"] = pd.to_numeric(df.get("descuento"), errors="coerce").fillna(0)

    invoice_dict["items"] = df.to_dict(orient="records")

    invoice_dict["estadisticas"] = {
        "cantidad_items": len(df),
        "item_mas_costoso": df.loc[df["precio_unitario"].idxmax(), "descripcion"] if not df.empty else None,
        "precio_promedio": round(df["precio_unitario"].mean(), 2),
    }

    return invoice_dict
