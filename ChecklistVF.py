import streamlit as st
from PIL import Image
from datetime import date
import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.styles import Alignment

# --- Título ---
st.set_page_config(page_title="Checklist Área de Planificación", page_icon="✅")
img = Image.open("logo.png")

# --- Título con imagen al lado ---
col1, col2 = st.columns([0.1, 1])  
col1.image(img, width=60)   
col2.markdown("## Checklist Área de Planificación")  

# --- Información del checklist ---
col1, col2, col3 = st.columns(3)

# Fecha
fecha_checklist = col1.date_input("📅 Fecha del checklist", value=date.today())

# Encargado
encargados = ["Brany Gómez", "Gerardo Muñoz", "Juan Pablo"]
encargado = col2.selectbox("👤 Encargado", encargados)

# Tienda
tiendas = ["Florida Center", "Plaza Oeste", "Costanera Center"]  # acortado por claridad
tienda = col3.selectbox("🏪 Tienda", tiendas)

st.markdown("---")  

st.subheader("Puntos a revisar")
# --- Lista de tareas ---
tareas = [
    "Cubicación vestuario",
    "Cubicación calzado",
    "Reposición (Curva, RAMI)",
    "Despachos",
    "Club Pillin",
    "Mix colección",
    "Visual merchandising",
    "Competencia",
    "Experiencia del cliente (CX)",
    "Dotación y gestión equipo de venta",
    "Posibles áreas de mejora"
]

# --- Estado de tareas ---
estado = []
valores_comentario = []
valores_opcion = []
opcion_cub = [70,75,80,85,90,95,100,105,110,115,120,125,130]

for tarea in tareas:
    checked = st.checkbox(tarea, key=f"chk_{tarea}")
    estado.append(checked)
    if tarea in ["Cubicación vestuario", "Cubicación calzado"]:
        opciones = st.selectbox(f"% Cub {tarea}", opcion_cub, index=6, key=f"opt_{tarea}")
        valores_opcion.append(opciones)
        valores_comentario.append("")
    else:
        comentario = st.text_input(f"Comentario para '{tarea}'", key=f"com_{tarea}")
        valores_opcion.append("")
        valores_comentario.append(comentario)

#

# --- Progreso ---
completadas = sum(estado)
total = len(tareas)
progreso = completadas / total if total > 0 else 0

st.progress(progreso)
st.write(f"Haz completado **{completadas} de {total} ítems**.")

faltantes = total - completadas
if completadas == total:
    st.success("🎉 ¡Checklist completo!")
elif completadas > 0:
    st.info(f"💪 Aún faltan **{faltantes}** puntos por abordar." )
else:
    st.warning("🙌 Aún no comienzas tu Checklist")
    
# --- Botón para guardar en Excel ---
if st.button("✅ Completado"):
    # Convertir fecha a string
    fecha_str = fecha_checklist.strftime("%Y-%m-%d")

    # Crear DataFrame
    df = pd.DataFrame({
        "Fecha": [fecha_str]*len(tareas),
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

    # Crear la celda combinada arriba
    titulo = f"Fecha: {fecha_str} | Encargado: {encargado} | Tienda: {tienda}"
    ws.insert_rows(1)  # inserta fila arriba
    ws.merge_cells("A1:G1")  # ajusta el rango según columnas
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





















