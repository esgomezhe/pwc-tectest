import json
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))

PROMPT = """Analiza el siguiente texto extraído de un documento (factura, tiquete o similar) y devuelve un JSON con la siguiente estructura. Si un campo no aplica o no se encuentra, usa null.

{
  "tipo_documento": "factura electrónica | tiquete | cuenta de cobro | otro",
  "numero_factura": "número o código del documento",
  "fecha_emision": "YYYY-MM-DD",
  "fecha_vencimiento": "YYYY-MM-DD o null",
  "emisor_nombre": "razón social o nombre comercial del emisor",
  "emisor_nit": "NIT o documento del emisor",
  "emisor_direccion": "dirección del emisor",
  "emisor_ciudad": "ciudad del emisor",
  "emisor_telefono": "teléfono del emisor",
  "cliente_nombre": "nombre del cliente o comprador",
  "cliente_documento": "NIT o cédula del cliente",
  "cliente_direccion": "dirección del cliente",
  "cliente_ciudad": "ciudad del cliente",
  "cliente_telefono": "teléfono del cliente",
  "cliente_email": "email del cliente o null",
  "condicion_pago": "contado | crédito | otro",
  "medio_pago": "efectivo | tarjeta crédito | tarjeta débito | transferencia | Nequi | otro",
  "moneda": "COP | USD | otro",
  "subtotal": 0.0,
  "descuento": 0.0,
  "impuestos": 0.0,
  "total": 0.0,
  "cufe": "código CUFE si existe o null",
  "resolucion_dian": "resolución DIAN si existe o null",
  "notas": "notas relevantes del documento o null",
  "resumen": "resumen ejecutivo de 2-3 líneas describiendo el documento",
  "items": [
    {
      "codigo": "código del producto o null",
      "descripcion": "descripción del ítem",
      "cantidad": 1.0,
      "unidad_medida": "UND | KG | otro o null",
      "precio_unitario": 0.0,
      "descuento": 0.0,
      "subtotal": 0.0
    }
  ]
}

Los valores numéricos deben ser números (float), no strings. Las fechas en formato YYYY-MM-DD.

Texto del documento:
"""


def analyze_invoice(text: str) -> dict:
    response = model.generate_content(
        PROMPT + text,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json"
        ),
    )
    return json.loads(response.text)
