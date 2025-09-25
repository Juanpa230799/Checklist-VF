import streamlit as st
from PIL import Image
from datetime import date
import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.styles import Alignment

# --- tu código de checklist arriba ---

if st.button("✅ Completado"):
    # Crear DataFrame combinando info general y checklist
    df = pd.DataFrame({
        "Fecha": [fecha_checklist]*len(tareas),
        "Encargado": [encargado]*len(tareas),
        "Tienda": [tienda]*len(tareas),
        "Tarea": tareas,
        "Completada": estado,
        "Valor": valores_opcion,
        "Comentario": valores_comentario
    })    

    # Guardar a Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Checklist")

    # Abrir con openpyxl para aplicar formato
    output.seek(0)
    wb = load_workbook(output)
    ws = wb.active

    # Crear la celda combinada arriba (fila 1)
    titulo = f"Fecha: {fecha_checklist} | Encargado: {encargado} | Tienda: {tienda}"
    ws.insert_rows(1)  # insertamos fila en blanco arriba
    ws.merge_cells("A1:G1")  # combina de A1 a G1 (ajusta si tu tabla es más ancha)
    ws["A1"] = titulo
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

    # Guardar cambios otra vez a BytesIO
    final_output = BytesIO()
    wb.save(final_output)
    final_output.seek(0)

    # Botón para descargar
    st.download_button(
        label="📥 Descargar checklist",
        data=final_output,
        file_name="Checklist_Completo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )





















