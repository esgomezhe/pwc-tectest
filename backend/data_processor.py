import pandas as pd


def process_invoice_data(invoice_dict: dict) -> dict:
    items = invoice_dict.get("items", [])
    if not items:
        invoice_dict["estadisticas"] = {
            "cantidad_items": 0,
            "item_mas_costoso": None,
            "item_mas_barato": None,
            "precio_promedio": 0,
            "total_descuentos": 0,
            "porcentaje_descuento": 0,
            "subtotal_calculado": 0,
            "distribucion_precio": {},
        }
        return invoice_dict

    df = pd.DataFrame(items)

    df["cantidad"] = pd.to_numeric(df.get("cantidad"), errors="coerce").fillna(0)
    df["precio_unitario"] = pd.to_numeric(df.get("precio_unitario"), errors="coerce").fillna(0)
    df["subtotal"] = pd.to_numeric(df.get("subtotal"), errors="coerce").fillna(0)
    df["descuento"] = pd.to_numeric(df.get("descuento"), errors="coerce").fillna(0)

    df["valor_bruto"] = df["cantidad"] * df["precio_unitario"]
    df["descuento_porcentual"] = df.apply(
        lambda row: round(row["descuento"] / row["valor_bruto"] * 100, 2) if row["valor_bruto"] > 0 else 0,
        axis=1,
    )
    total_subtotal = df["subtotal"].sum()
    df["participacion"] = df["subtotal"].apply(
        lambda x: round(x / total_subtotal * 100, 2) if total_subtotal > 0 else 0
    )

    invoice_dict["items"] = df.to_dict(orient="records")

    stats = df["precio_unitario"].describe()

    invoice_dict["estadisticas"] = {
        "cantidad_items": int(len(df)),
        "cantidad_unidades": int(df["cantidad"].sum()),
        "item_mas_costoso": df.loc[df["precio_unitario"].idxmax(), "descripcion"],
        "item_mas_barato": df.loc[df["precio_unitario"].idxmin(), "descripcion"],
        "precio_promedio": round(stats["mean"], 2),
        "precio_mediana": round(stats["50%"], 2),
        "precio_maximo": round(stats["max"], 2),
        "precio_minimo": round(stats["min"], 2),
        "desviacion_estandar": round(stats["std"], 2) if len(df) > 1 else 0,
        "total_descuentos": round(df["descuento"].sum(), 2),
        "porcentaje_descuento": round(
            (df["descuento"].sum() / df["valor_bruto"].sum() * 100) if df["valor_bruto"].sum() > 0 else 0, 2
        ),
        "subtotal_calculado": round(df["subtotal"].sum(), 2),
        "valor_bruto_total": round(df["valor_bruto"].sum(), 2),
        "distribucion_precio": {
            row["descripcion"]: round(row["participacion"], 2)
            for _, row in df.iterrows()
        },
    }

    return invoice_dict
