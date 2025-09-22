import streamlit as st
from PIL import Image
from datetime import date
import pandas as pd
from io import BytesIO

# --- OneDrive ---
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential

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
tiendas = [
    "Plaza Oeste",
    "Florida Center",
    "Plaza Alameda",
    "Plaza Sur",
    "Portal Rancagua",
    "Plaza Trebol",
    "Plaza Vespucio",
    "Plaza Los Angeles",
    "Plaza Norte",
    "Apumanque",
    "Portal Ñuñoa",
    "Plaza Calama",
    "Plaza Antofagasta",
    "Portal Temuco",
    "Arauco Premium Outlet",
    "Paseo Viña Centro",
    "Costanera Center",
    "Plaza Bio Bio",
    "Arauco Maipu",
    "Mall del Centro Concepcion",
    "Plaza Tobalaba",
    "Portal Osorno",
    "Arauco Quilicura",
    "Plaza Copiapo",
    "Plaza Egaña",
    "Open Plaza Ovalle",
    "Easton Quilicura",
    "Vivo Outlet Maipú",
    "Plaza Iquique",
    "Vivo Los Trapenses",
    "Gran Avenida Esp.Urbano",
    "San Pedro Arauco Outlet",
    "Portal Centro Talca",
    "Mall Valle Curico",
    "Arauco Chillan",
    "Midmall Outlet",
    "Paseo Estado",
    "Paseo Chiloé",
    "La Fábrica Patio Outlet",
    "Vivo Outlet Peñuelas",
    "Viña Outlet Park",
    "Valdivia Centro",
    "Vivo San Fernando",
    "Parque Arauco",
    "Vivo Outlet La Florida",
    "Portal Valdivia",
    "Patio Rancagua",
    "Vivo Coquimbo",
    "Vivo Outlet Temuco",
    "Arauco Coronel",
    "Mall Barrio Independencia",
    "Outlet Style",
    "Easton Temuco",
    "PATRONATO 403",
    "Portal El Llano",
    "Paseo Alerce",
    "Santa Filomena 540",
    "Antofagasta Outlet Espacio Urbano",
    "Paseo Costanera Puerto Montt",
    "Paseo Puerto Varas",
    "Vivo Outlet Chillan",
    "Curauma Outlet",
    "15 Norte Viña",
    "Talca Outlet Go Florida",
    "Pionero Punta Arenas",
    "Rancagua Outlet Mall",
    "Mall Paseo San Bernardo",
    "Paseo Quillota",
    "Easton Segundo Piso"
]

tienda = col3.selectbox("🏪 Tienda", tiendas)

st.markdown("---")  # separador

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
    if tarea == "Cubicación vestuario":
        opciones = st.selectbox(f"% Cub", opcion_cub, index=6, key=f"opt_{tarea}")
        valores_opcion.append(opciones)
        valores_comentario.append("")
    elif tarea == "Cubicación calzado":
        opciones = st.selectbox(f"% Cub", opcion_cub, index=6, key=f"opt_{tarea}")
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
st.write(f"Haz completado **{completadas} de {total} ítems**.")

# --- Mensaje motivador ---
faltantes = total - completadas
if completadas == total:
    st.success("🎉 ¡Checklist completo!")
elif completadas > 0:
    st.info(f"💪 Aún faltan **{faltantes}** puntos por abordar." )
else:
    st.warning("🙌 Aún no comienzas tu Checklist")

# --- OneDrive Config ---
site_url = "https://1drv.ms/x/c/41dd00801bd46bea/EeCFp_G5FYNHm-VwvMwy_AEBau-PMXaCBdkEET-EbCd06A?e=vnpN7T"
folder_url = "https://onedrive.live.com/?login_hint=jppereiran23%40hotmail%2Ecom&view=1"
file_name = "Checklist_Completo.xlsx"
user = "jppereiran23@hotmail.com"
app_password = "rizbwsdnanryoift"  # Reemplaza por tu contraseña de aplicación
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
    try:
        # Conexión a OneDrive
        ctx = ClientContext(site_url).with_credentials(UserCredential(user, app_password))

        # Descargar Excel existente
        file = ctx.web.get_folder_by_server_relative_url(folder_url).get_file(file_name).download().execute_query()
        excel_bytes = BytesIO(file.content)
        df_existente = pd.read_excel(excel_bytes, sheet_name="Checklist")

        # Agregar nueva fila
        df_actualizado = pd.concat([df_existente, df], ignore_index=True)
        
        # Guardar a Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Checklist")

    # Subir archivo actualizado
        ctx.web.get_folder_by_server_relative_url(folder_url).upload_file(file_name, output.getvalue()).execute_query()
        st.success("📤 Checklist guardado en OneDrive exitosamente")
    #processed_data = output.getvalue()

    # Botón para descargar
    except Exception as e:
        st.error(f"❌ Error al subir a OneDrive: {e}")
   # st.download_button(
    #    label="📥 Descargar checklist",
     #   data=processed_data,
      #  file_name="Checklist_Completo.xlsx",
       # mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
   # )




















