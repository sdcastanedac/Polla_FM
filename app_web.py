import streamlit as st
import pandas as pd
import os

# ----------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ----------------------------------------
st.set_page_config(page_title="Polla Mundialista", page_icon="⚽", layout="wide")

# Diseño CSS personalizado (Estilo Premium, Limpio y Tonos Pasteles)
st.markdown("""
    <style>
    /* Fondo general de la app (Gris neutro muy suave / Off-white) */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Textos principales en gris oscuro/azul oscuro para excelente lectura */
    h1, h2, h3, p, span {
        color: #1e293b !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Estilo del Título Principal */
    .titulo-principal {
        color: #0f172a !important;
        font-weight: 800;
        font-size: 2.6em;
        margin-bottom: 5px;
        line-height: 1.2;
    }
    
    /* Subtítulo en tono pastel/neutro azulado */
    .subtitulo {
        color: #64748b !important;
        font-size: 1.3em;
        font-weight: 400;
        margin-top: 0px;
        margin-bottom: 25px;
    }
    
    /* Ajuste fino para los bordes y contenedores de las métricas */
    div[data-testid="stMetricSimpleValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# ENCABEZADO (Escudo superior izquierdo + Títulos)
# ----------------------------------------
# Usamos columnas para posicionar el escudo a la izquierda y el texto al lado
col_escudo, col_texto = st.columns([1, 5])

with col_escudo:
    # Reemplaza esta URL por el enlace directo de la imagen del escudo que desees usar
    # También puedes subir un archivo 'escudo.png' a GitHub y escribir aquí "escudo.png"
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
color_grafica = "#3b82f6" # Azul pastel/tecnológico por defecto

if os.path.exists(ruta_eliminatorias):
    df = pd.read_csv(ruta_eliminatorias)
    fase_actual = "Clasificación General (Fase de Grupos + Eliminatorias)"
    columna_orden = 'Total_General'
    color_grafica = "#0284c7" # Azul cielo profundo para eliminatorias
elif os.path.exists(ruta_grupos):
    df = pd.read_csv(ruta_grupos)
    fase_actual = "Clasificación - Fase de Grupos"
    columna_orden = 'Puntos_Grupos'
    color_grafica = "#f59e0b" # Dorado/Ámbar suave para grupos
else:
    st.warning("Esperando la carga de los primeros resultados consolidados...")

# ----------------------------------------
# VISUALIZACIONES EN PANTALLA
# ----------------------------------------
if df is not None:
    st.markdown(f"#### 📍 Etapa Actual: **{fase_actual}**")
    
    # 1. SECCIÓN DEL PODIO (Tarjetas limpias con fondo claro)
    st.markdown("### 🏆 Líderes de la Jornada")
    col1, col2, col3 = st.columns(3)
    
    # Formato amigable para destacar los 3 primeros lugares
    if len(df) >= 1:
        col2.background_color = "#ffffff"
        col2.metric("🥇 1er Puesto", df.iloc[0]['Participante'], f"{df.iloc[0][columna_orden]} Puntos")
    if len(df) >= 2:
        col1.metric("🥈 2do Puesto", df.iloc[1]['Participante'], f"{df.iloc[1][columna_orden]} Puntos")
    if len(df) >= 3:
        col3.metric("🥉 3er Puesto", df.iloc[2]['Participante'], f"{df.iloc[2][columna_orden]} Puntos")
        
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. GRÁFICA DE BARRAS (Ahora limpia y con fondo claro nativo)
    st.markdown("### 📊 Tendencia de Puntuaciones")
    df_grafica = df.set_index('Participante')
    # Al estar sobre fondo claro, la gráfica se dibuja automáticamente sin cuadros negros oscuros
    st.bar_chart(df_grafica[columna_orden], color=color_grafica)
    
    st.divider()

    # 3. TABLA DE POSICIONES COMPLETA
    st.markdown("### 📋 Tabla General de Posiciones")
    # Mostramos la tabla con un sutil resalte verde pastel en el puntaje máximo
    st.dataframe(
        df.style.highlight_max(subset=[columna_orden], color='#bbf7d0')
                .format(precision=0),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("<p style='text-align: center; color: #94a3b8 !important; font-size: 0.9em;'>Actualización automática al día con los resultados oficiales de la mesa técnica.</p>", unsafe_allow_html=True)