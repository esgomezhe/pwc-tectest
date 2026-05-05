# Invoice Analyzer

Herramienta web full-stack que permite subir una factura en PDF, extraer su información automáticamente con IA (Gemini), persistir los resultados en una base de datos y consultar el historial de facturas analizadas.

Prueba técnica para el cargo de Analista de TI JR en PwC Colombia.

## Stack

- **Backend:** FastAPI, PyMuPDF, Pandas, Gemini API, SQLAlchemy + SQLite
- **Frontend:** React (JavaScript), Axios, React Router DOM, Tailwind CSS (CDN)

## Uso

1. Sube una factura en PDF desde la interfaz
2. El sistema extrae el texto, lo analiza con Gemini y estructura los datos
3. Los resultados se muestran en pantalla y se guardan en la base de datos
4. Consulta el historial de facturas analizadas en el panel izquierdo
