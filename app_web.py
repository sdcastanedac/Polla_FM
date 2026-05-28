import streamlit as st
import pandas as pd
import os
import altair as alt  # <-- Nueva librería para gráficas avanzadas

# ----------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ----------------------------------------
st.set_page_config(page_title="Polla Mundialista", page_icon="⚽", layout="wide")

# Diseño CSS personalizado (Garantiza fondo claro y textos oscuros legibles)
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    h1, h2, h3, p, span {
        color: #1e293b !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .titulo-principal {
        color: #0f172a !important;
        font-weight: 800;
        font-size: 2.6em;
        margin-bottom: 5px;
        line-height: 1.2;
    }
    .subtitulo {
        color: #64748b !important;
        font-size: 1.3em;
        font-weight: 400;
        margin-top: 0px;
        margin-bottom: 25px;
    }
    div[data-testid="stMetricSimpleValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# ENCABEZADO
# ----------------------------------------
col_escudo, col_texto = st.columns([1, 5])

with col_escudo:
    url_escudo = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Escudo_del_Banco_de_la_Rep%C3%BAblica_de_Colombia.svg"
    st.image(url_escudo, width=110)

with col_texto:
    st.markdown("<h1 class='titulo-principal'>GRAN POLLA MUNDIALISTA FÁBRICA DE MONEDA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo'>⚽ Panel Oficial de Resultados y Posiciones - En Vivo</p>", unsafe_allow_html=True)

st.divider()

# ----------------------------------------
# CARGA DE DATOS
# ----------------------------------------
ruta_eliminatorias = 'Ranking_General_Acumulado.csv'
ruta_grupos = 'Ranking_Diario_Fase_Grupos.csv'

df = None
fase_actual = ""
color_grafica = "#3b82f6" 

if os.path.exists(ruta_eliminatorias):
    df = pd.read_csv(ruta_eliminatorias)
    fase_actual = "Clasificación General (Fase de Grupos + Eliminatorias)"
    columna_orden = 'Total_General'
    color_grafica = "#0284c7" # Azul cielo profundo
elif os.path.exists(ruta_grupos):
    df = pd.read_csv(ruta_grupos)
    fase_actual = "Clasificación - Fase de Grupos"
    columna_orden = 'Puntos_Grupos'
    color_grafica = "#f59e0b" # Dorado pastel
else:
    st.warning("Esperando la carga de los primeros resultados consolidados...")

# ----------------------------------------
# VISUALIZACIONES EN PANTALLA
# ----------------------------------------
if df is not None:
    st.markdown(f"#### 📍 Etapa Actual: **{fase_actual}**")
    
    # 1. EL PODIO
    st.markdown("### 🏆 Líderes de la Jornada")
    col1, col2, col3 = st.columns(3)
    
    if len(df) >= 1:
        col2.metric("🥇 1er Puesto", df.iloc[0]['Participante'], f"{df.iloc[0][columna_orden]} Puntos")
    if len(df) >= 2:
        col1.metric("🥈 2do Puesto", df.iloc[1]['Participante'], f"{df.iloc[1][columna_orden]} Puntos")
    if len(df) >= 3:
        col3.metric("🥉 3er Puesto", df.iloc[2]['Participante'], f"{df.iloc[2][columna_orden]} Puntos")
        
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. GRÁFICA AVANZADA (SIN FONDO NEGRO Y CON EJES CLAROS)
    st.markdown("### 📊 Tendencia de Puntuaciones")
    
    # Configuración de la gráfica forzando estilo claro y bordes redondeados
    grafica = alt.Chart(df).mark_bar(
        color=color_grafica, 
        cornerRadiusTopLeft=4, 
        cornerRadiusTopRight=4,
        size=40 # Grosor de las barras
    ).encode(
        x=alt.X('Participante:N', 
                sort='-y', # Ordenar de mayor a menor puntaje
                axis=alt.Axis(
                    labelAngle=-45, 
                    labelColor="#1e293b", # Texto del eje X gris oscuro
                    title="Participantes",
                    titleColor="#1e293b",
                    labelFontSize=12,
                    grid=False # Sin rayas verticales de fondo
                )),
        y=alt.Y(f'{columna_orden}:Q', 
                axis=alt.Axis(
                    labelColor="#1e293b", # Texto del eje Y gris oscuro
                    title="Puntos",
                    titleColor="#1e293b",
                    gridColor="#e2e8f0", # Líneas guía de fondo muy suaves
                    labelFontSize=12
                )),
        tooltip=['Participante', alt.Tooltip(f'{columna_orden}:Q', title='Puntos')]
    ).properties(
        height=400,
        background='transparent' # Se adapta perfectamente al color de la app
    )

    # ¡IMPORTANTE!: theme=None es lo que impide que Streamlit lo ponga negro en modo oscuro
    st.altair_chart(grafica, use_container_width=True, theme=None)
    
    st.divider()

    # 3. TABLA DE POSICIONES COMPLETA
    st.markdown("### 📋 Tabla General de Posiciones")
    st.dataframe(
        df.style.highlight_max(subset=[columna_orden], color='#bbf7d0')
                .format(precision=0),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("<p style='text-align: center; color: #94a3b8 !important; font-size: 0.9em;'>Actualización automática al día con los resultados oficiales de la mesa técnica.</p>", unsafe_allow_html=True)