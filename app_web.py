import streamlit as st
import pandas as pd
import os

# ----------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ----------------------------------------
st.set_page_config(page_title="Polla Mundialista", page_icon="⚽", layout="wide")

# Diseño CSS personalizado (Cancha de fútbol y colores)
st.markdown("""
    <style>
    .stApp {
        background-color: #1a472a; /* Verde césped oscuro */
        background-image: url("https://www.transparenttextures.com/patterns/grass.png");
    }
    h1, h2, h3, p {
        color: #ffffff !important;
        font-family: 'Arial Black', sans-serif;
    }
    .titulo-principal {
        text-align: center;
        color: #FFD700 !important; /* Dorado */
        text-shadow: 2px 2px 4px #000000;
        font-size: 3em;
        margin-bottom: 0;
    }
    .subtitulo {
        text-align: center;
        color: #ffffff !important;
        font-size: 1.5em;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# ENCABEZADO
# ----------------------------------------
st.markdown("<h1 class='titulo-principal'>🏆 GRAN POLLA MUNDIALISTA FÁBRICA DE MONEDA ⚽</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo'>Tabla de Posiciones Oficial - Mundial 2026</p>", unsafe_allow_html=True)

# ----------------------------------------
# CARGA DE DATOS
# ----------------------------------------
# El sistema busca primero si ya hay resultados de eliminatorias, sino, muestra los de grupos
ruta_eliminatorias = 'Ranking_General_Acumulado.csv'
ruta_grupos = 'Ranking_Diario_Fase_Grupos.csv'

df = None
fase_actual = ""

if os.path.exists(ruta_eliminatorias):
    df = pd.read_csv(ruta_eliminatorias)
    fase_actual = "Clasificación General (Grupos + Eliminatorias)"
    columna_orden = 'Total_General'
elif os.path.exists(ruta_grupos):
    df = pd.read_csv(ruta_grupos)
    fase_actual = "Clasificación Fase de Grupos"
    columna_orden = 'Puntos_Grupos'
else:
    st.warning("Aún no se han calculado resultados. Ejecuta el script de cálculo primero.")

# ----------------------------------------
# VISUALIZACIONES
# ----------------------------------------
if df is not None:
    st.markdown(f"### 📍 Fase Actual: {fase_actual}")
    
    # 1. EL PODIO (Métricas destacadas)
    st.markdown("### 🥇 El Podio Actual")
    col1, col2, col3 = st.columns(3)
    
    if len(df) >= 1:
        col2.metric("🥇 1er Lugar", df.iloc[0]['Participante'], f"{df.iloc[0][columna_orden]} pts")
    if len(df) >= 2:
        col1.metric("🥈 2do Lugar", df.iloc[1]['Participante'], f"{df.iloc[1][columna_orden]} pts")
    if len(df) >= 3:
        col3.metric("🥉 3er Lugar", df.iloc[2]['Participante'], f"{df.iloc[2][columna_orden]} pts")
        
    st.divider()

    # 2. GRÁFICA DE BARRAS
    st.markdown("### 📊 Gráfica de Rendimiento")
    # Preparamos los datos para la gráfica
    df_grafica = df.set_index('Participante')
    st.bar_chart(df_grafica[columna_orden], color="#FFD700") # Gráfica dorada
    
    st.divider()

    # 3. TABLA DE POSICIONES COMPLETA
    st.markdown("### 📋 Tabla de Posiciones Detallada")
    # Damos formato a la tabla para que se vea atractiva
    st.dataframe(
        df.style.highlight_max(subset=[columna_orden], color='#2e7d32')
                .format(precision=0),
        use_container_width=True,
        hide_index=True
    )
    
    st.success("Tus datos están actualizados. ¡Que gane el mejor estratega!")