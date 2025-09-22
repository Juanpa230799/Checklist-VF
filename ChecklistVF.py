import streamlit as st
from PIL import Image
from datetime import date
import pandas as pd
from io import BytesIO

# --- Título ---
st.set_page_config(page_title="Checklist Área de Planificación", page_icon="✅")
#img = Image.open(r"C:\\Users\\JPEREIRA\\OneDrive - PILLIN S.A\\Escritorio\\Checklist\\logo.png")  
img = Image.open("logo.png")
# --- Título con imagen al lado ---
col1, col2 = st.columns([0.1, 1])  # Ajusta el tamaño relativo
col1.image(img, width=60)   # Reemplaza "logo.png" por el nombre de tu archivo de imagen
col2.markdown("## Checklist Área de Planificación")  # Markdown para simular título

#st.title("Checklist Área de Planificación")
#st.image("logo.png", width=50)  # Ajusta el width según necesites

# --- Información del checklist ---
col1, col2, col3 = st.columns(3)

# Fecha
fecha_checklist = col1.date_input("📅 Fecha del checklist", value=date.today())

# Encargado
encargados = ["Brany Gómez", "Gerardo Muñoz", "Juan Pablo"]  # aquí pones tu lista de encargados
encargado = col2.selectbox("👤 Encargado", encargados)

# Tienda
tiendas = [""] + [
    "Plaza Calama",
    "Plaza Antofagasta",
    "Plaza Copiapo",
    "Open Plaza Ovalle",
    "Plaza Iquique",
    "Vivo Coquimbo",
    "15 Norte Viña",
    "Mall Paseo San Bernardo",
    "Plaza Oeste",
    "Florida Center",
    "Plaza Alameda",
    "Plaza Sur",
    "Portal Rancagua",
    "Plaza Vespucio",
    "Plaza Norte",
    "Apumanque",
    "Portal Ñuñoa",
    "Paseo Viña Centro",
    "Costanera Center",
    "Arauco Maipu",
    "Plaza Tobalaba",
    "Arauco Quilicura",
    "Plaza Egaña",
    "Vivo Los Trapenses",
    "Gran Avenida Esp.Urbano",
    "Paseo Estado",
    "Vivo San Fernando",
    "Parque Arauco",
    "Patio Rancagua",
    "Mall Barrio Independencia",
    "PATRONATO 403",
    "Portal El Llano",
    "Paseo Costanera Puerto Montt",
    "Paseo Puerto Varas",
    "Pionero Punta Arenas",
    "Plaza Trebol",
    "Plaza Los Angeles",
    "Portal Temuco",
    "Plaza Bio Bio",
    "Mall del Centro Concepcion",
    "Portal Osorno",
    "Portal Centro Talca",
    "Mall Valle Curico",
    "Arauco Chillan",
    "Paseo Chiloé",
    "Portal Valdivia",
    "Antofagasta Outlet Espacio Urbano",
    "Vivo Outlet Peñuelas",
    "Curauma Outlet",
    "Arauco Premium Outlet",
    "Easton Quilicura",
    "Vivo Outlet Maipú",
    "Midmall Outlet",
    "La Fábrica Patio Outlet",
    "Viña Outlet Park",
    "Vivo Outlet La Florida",
    "Outlet Style",
    "Easton Segundo Piso",
    "Vivo Outlet Chillan",
    "Talca Outlet Go Florida",
    "San Pedro Arauco Outlet",
    "Vivo Outlet Temuco",
    "Arauco Coronel",
    "Easton Temuco",
    "Paseo Alerce",
    "Paseo Quillota",
    "Valdivia Centro",
    "Santa Filomena 540",
    "Rancagua Outlet Mall",
]
tienda = col3.selectbox("🏪 Tienda", tiendas)

st.markdown("---")  # separador

st.subheader("Puntos a revisar")
# --- Lista de tareas ---
tareas = [
    "Cubicación",
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

opcion_cub = [""] + [70,75,80,85,90,95,100,105,110,115,120,125,130]

for tarea in tareas:

    checked = st.checkbox(tarea, key=f"chk_{tarea}")
    estado.append(checked)

    if tarea == "Cubicación":
        opciones = st.selectbox(f"% Cub", opcion_cub, key=f"opt_{tarea}")
        valores_opcion.append(opciones)
        valores_comentario.append("")
    else:
        #checked = st.checkbox(tarea)
        #estado.append(checked)
        comentario = st.text_input(f"Comentario para '{tarea}'", key=f"com_{tarea}")
        valores_opcion.append("")
        valores_comentario.append(comentario)
# --- Progreso ---
completadas = sum(estado)
total = len(tareas)
progreso = completadas / total if total > 0 else 0

st.progress(progreso)
st.write(f"Has completado **{completadas} de {total} tareas**.")

# --- Mensaje motivador ---
if completadas == total:
    st.success("🎉 ¡Excelente! Completaste todo el checklist.")
elif completadas > 0:
    st.info("💪 Vas avanzando, sigue así.")
else:
    st.warning("🙌 Aún no comienzas, ¡manos a la obra!")

# --- Botón para guardar en Excel ---
if st.button("✅ Completado"):

    # Crear DataFrame combinando info general y checklist
    df = pd.DataFrame({
        "Fecha": [fecha_checklist]*len(tareas),
        "Encargado": [encargado]*len(tareas),
        "Tienda": [tienda]*len(tareas),
        "Tarea": tareas,
        "Completada": estado,
        "Valor": valores_opcion,       # columna nueva
        "Comentario": valores_comentario  # columna nueva
    })

    # Guardar a Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Checklist")
    
    processed_data = output.getvalue()

    # Botón para descargar
    st.download_button(
        label="📥 Descargar checklist",
        data=processed_data,
        file_name="Checklist_Completo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )




