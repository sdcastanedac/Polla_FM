import streamlit as st
import pandas as pd
import os
import altair as alt

# ----------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ----------------------------------------
st.set_page_config(page_title="Polla Mundialista Callejera", page_icon="⚽", layout="wide")

# PALETA DE COLORES INSTITUCIONAL
COLOR_PRINCIPAL = "#003870"  
COLOR_ACCENTO = "#D4AF37"     
COLOR_FONDO = "#F4F6F9"       
COLOR_TEXTO = "#1A2530"       

# Estilos CSS Unificados
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_FONDO}; }}
    h1, h2, h3, h4, p, span, label {{
        color: {COLOR_TEXTO} !important;
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif !important;
    }}
    .titulo-principal {{
        color: {COLOR_PRINCIPAL} !important;
        font-weight: 800;
        font-size: 2.4em;
        margin: 0;
        line-height: 1.1;
    }}
    .subtitulo {{
        color: #5A6A85 !important;
        font-size: 1.2em;
        font-weight: 400;
        margin: 5px 0 0 0;
    }}
    div[data-testid="stMetric"] {{
        background-color: #ffffff !important;
        border: 1px solid #E2E8F0 !important;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    div[data-testid="stMetricSimpleValue"] {{
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        color: {COLOR_PRINCIPAL} !important;
    }}
    .tabla-contenedor {{
        background-color: #ffffff;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        height: 380px;
        overflow-y: auto;
    }}
    .tabla-polla {{
        width: 100%;
        border-collapse: collapse;
        background-color: #ffffff !important;
        color: {COLOR_TEXTO} !important;
        font-size: 13px;
        text-align: left;
    }}
    .tabla-polla th {{
        background-color: {COLOR_PRINCIPAL} !important;
        color: #ffffff !important;
        padding: 12px 10px;
        font-weight: 600;
        position: sticky;
        top: 0;
    }}
    .tabla-polla td {{
        padding: 10px;
        border-bottom: 1px solid #E2E8F0;
        color: {COLOR_TEXTO} !important;
        background-color: #ffffff !important;
    }}
    .tabla-polla tr:nth-child(1) td {{
        background-color: #DCE6F1 !important; 
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# ENCABEZADO
# ----------------------------------------
if os.path.exists("mascotas2026.png"):
    col_img, col_tit = st.columns([1, 8])
    with col_img:
        st.image("mascotas2026.png", width=100)
    with col_tit:
        st.markdown(f"<h1 class='titulo-principal'>GRAN POLLA MUNDIALISTA CALLEJERA</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitulo'>⚽ Panel Oficial de Resultados y Posiciones en Tiempo Real</p>", unsafe_allow_html=True)
else:
    url_alternativa = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Escudo_del_Banco_de_la_Rep%C3%BAblica_de_Colombia.svg/512px-Escudo_del_Banco_de_la_Rep%C3%BAblica_de_Colombia.svg.png"
    col_img, col_tit = st.columns([1, 8])
    with col_img:
        st.image(url_alternativa, width=100)
    with col_tit:
        st.markdown(f"<h1 class='titulo-principal'>GRAN POLLA MUNDIALISTA CALLEJERA</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitulo'>⚽ Panel Oficial de Resultados y Posiciones en Tiempo Real</p>", unsafe_allow_html=True)

st.divider()

# ----------------------------------------
# CARGA DE RANKING (DATOS DE POSICIONES)
# ----------------------------------------
ruta_eliminatorias = 'Ranking_General_Acumulado.csv'
ruta_grupos = 'Ranking_Diario_Fase_Grupos.csv'
archivo_reales_elim = 'Resultados_Reales_Eliminatorias.xlsx'
archivo_reales_grupos = 'Resultados_Reales_Grupos.xlsx'

df = None
fase_actual = ""

if os.path.exists(ruta_eliminatorias):
    df = pd.read_csv(ruta_eliminatorias)
    fase_actual = "Clasificación General (Fase de Grupos + Eliminatorias)"
    columna_orden = 'Total_General'
elif os.path.exists(ruta_grupos):
    df = pd.read_csv(ruta_grupos)
    fase_actual = "Clasificación - Fase de Grupos"
    columna_orden = 'Puntos_Grupos'

# ----------------------------------------
# 1. SECCIÓN DE PODIO Y TABLAS
# ----------------------------------------
if df is not None:
    st.markdown(f"#### 📍 Etapa del Torneo: **{fase_actual}**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    if len(df) >= 1: col2.metric("🥇 1er Puesto", df.iloc[0]['Participante'], f"{int(df.iloc[0][columna_orden])} Puntos")
    if len(df) >= 2: col1.metric("🥈 2do Puesto", df.iloc[1]['Participante'], f"{int(df.iloc[1][columna_orden])} Puntos")
    if len(df) >= 3: col3.metric("🥉 3er Puesto", df.iloc[2]['Participante'], f"{int(df.iloc[2][columna_orden])} Puntos")
        
    st.markdown("<br>", unsafe_allow_html=True)

    col_grafica, col_tabla = st.columns([1, 1])

    with col_grafica:
        st.markdown("### 📊 Tendencia de Puntuaciones")
        grafica = alt.Chart(df).mark_bar(color=COLOR_PRINCIPAL, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X('Participante:N', sort='-y', axis=alt.Axis(labelAngle=-45, labelColor=COLOR_TEXTO, title="", grid=False)),
            y=alt.Y(f'{columna_orden}:Q', axis=alt.Axis(labelColor=COLOR_TEXTO, title="Puntuación Total", gridColor="#E2E8F0")),
            tooltip=['Participante', alt.Tooltip(f'{columna_orden}:Q', title='Puntos')]
        ).properties(height=380, background='transparent')
        st.altair_chart(grafica, use_container_width=True, theme=None)

    with col_tabla:
        st.markdown("### 📋 Tabla de Posiciones Consolidada")
        html_tabla = f"<div class='tabla-contenedor'><table class='tabla-polla'><thead><tr>"
        for col in df.columns: html_tabla += f"<th>{col}</th>"
        html_tabla += "</tr></thead><tbody>"
        for _, row in df.iterrows():
            html_tabla += "<tr>"
            for col in df.columns:
                val = int(row[col]) if isinstance(row[col], (float, int)) else row[col]
                html_tabla += f"<td>{val}</td>"
            html_tabla += "</tr>"
        html_tabla += "</tbody></table></div>"
        st.markdown(html_tabla, unsafe_allow_html=True)
    
    st.divider()

# ----------------------------------------
# 2. SECCIÓN DE RESULTADOS EN VIVO / FIXTURE
# ----------------------------------------
st.markdown("### 🏟️ Marcadores Oficiales y Fixture")

# Función auxiliar para renderizar tarjetas de partidos
def crear_tarjeta_partido(local, visita, goles_l, goles_v, info_extra=""):
    tarjeta = f"""
    <div style='border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; min-width: 280px; max-width: 300px; background-color: #ffffff; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 10px;'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
            <span style='font-weight: 600; color: {COLOR_TEXTO}; font-size: 14px;'>{local}</span>
            <span style='background-color: #F1F5F9; padding: 2px 10px; border-radius: 4px; font-weight: bold; color: {COLOR_PRINCIPAL};'>{goles_l}</span>
        </div>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-weight: 600; color: {COLOR_TEXTO}; font-size: 14px;'>{visita}</span>
            <span style='background-color: #F1F5F9; padding: 2px 10px; border-radius: 4px; font-weight: bold; color: {COLOR_PRINCIPAL};'>{goles_v}</span>
        </div>
    """
    if info_extra:
        tarjeta += f"<div style='margin-top: 10px; font-size: 12px; color: #10B981; font-weight: bold; text-align: center; border-top: 1px solid #E2E8F0; padding-top: 8px;'>✅ Avanza: {info_extra}</div>"
    tarjeta += "</div>"
    return tarjeta

# A. Si estamos en ELIMINATORIAS
if os.path.exists(archivo_reales_elim):
    df_reales = pd.read_excel(archivo_reales_elim)
    # Filtramos partidos donde ya se sabe quiénes se enfrentan
    df_fixture = df_reales.dropna(subset=['Equipo Local', 'Equipo Visitante'])
    
    if not df_fixture.empty:
        fases = df_fixture['Fase'].unique()
        for fase in fases:
            st.markdown(f"#### 🏆 {fase}")
            df_fase = df_fixture[df_fixture['Fase'] == fase]
            
            html_partidos = "<div style='display: flex; flex-wrap: wrap; gap: 15px;'>"
            for _, row in df_fase.iterrows():
                g_l = int(row['Goles L']) if pd.notna(row['Goles L']) else "-"
                g_v = int(row['Goles V']) if pd.notna(row['Goles V']) else "-"
                clasificado = row['Clasificado a sig. ronda'] if pd.notna(row['Clasificado a sig. ronda']) else ""
                html_partidos += crear_tarjeta_partido(row['Equipo Local'], row['Equipo Visitante'], g_l, g_v, clasificado)
            html_partidos += "</div><br>"
            st.markdown(html_partidos, unsafe_allow_html=True)
    else:
        st.info("Aún no se han definido las llaves de las rondas eliminatorias.")

# B. Si estamos en FASE DE GRUPOS
elif os.path.exists(archivo_reales_grupos):
    df_reales = pd.read_excel(archivo_reales_grupos)
    # Mostramos solo los partidos que YA tienen marcadores ingresados
    df_jugados = df_reales.dropna(subset=['Goles L', 'Goles V'])
    
    if not df_jugados.empty:
        grupos = df_jugados['Grupo'].unique()
        for grupo in grupos:
            st.markdown(f"#### ⚽ {grupo}")
            df_g = df_jugados[df_jugados['Grupo'] == grupo]
            
            html_partidos = "<div style='display: flex; flex-wrap: wrap; gap: 15px;'>"
            for _, row in df_g.iterrows():
                g_l = int(row['Goles L'])
                g_v = int(row['Goles V'])
                html_partidos += crear_tarjeta_partido(row['Equipo Local'], row['Equipo Visitante'], g_l, g_v)
            html_partidos += "</div><br>"
            st.markdown(html_partidos, unsafe_allow_html=True)
    else:
        st.info("Aún no hay marcadores registrados en la Fase de Grupos. ¡A la espera del partido inaugural!")
else:
    st.info("No se encontró archivo de resultados reales. Recuerda subir el Excel a GitHub.")
