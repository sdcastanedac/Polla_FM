import streamlit as st
import pandas as pd
import os
import altair as alt

# ----------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ----------------------------------------
st.set_page_config(page_title="Polla Mundialista Fábrica de Moneda", page_icon="⚽", layout="wide")

# PALETA DE COLORES HOMOGÉNEA (Estilo Institucional)
COLOR_PRINCIPAL = "#003870"  # Azul Marino Corporativo
COLOR_ACCENTO = "#D4AF37"     # Oro/Dorado para destaques
COLOR_FONDO = "#F4F6F9"       # Gris claro neutro
COLOR_TEXTO = "#1A2530"       # Gris oscuro para lectura limpia

# Aplicación de estilos CSS unificados
st.markdown(f"""
    <style>
    /* Fondo general de la aplicación */
    .stApp {{
        background-color: {COLOR_FONDO};
    }}
    
    /* Tipografía y colores de textos */
    h1, h2, h3, h4, p, span, label {{
        color: {COLOR_TEXTO} !important;
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif !important;
    }}
    
    /* Contenedor del Título Principal */
    .header-container {{
        display: flex;
        align-items: center;
        gap: 20px;
        padding-bottom: 15px;
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
    
    /* Estilo homogéneo para las tarjetas del Podio */
    div[data-testid="stMetric"] {{
        background-color: #ffffff;
        border: 1px solid #E2E8F0;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    
    div[data-testid="stMetricSimpleValue"] {{
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        color: {COLOR_PRINCIPAL} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# ENCABEZADO OPTIMIZADO (Escudo + Títulos)
# ----------------------------------------
# Intentará cargar 'escudo.png' desde tu GitHub; si no existe, usa un diseño de respaldo limpio
if os.path.exists("escudo.png"):
    col_img, col_tit = st.columns([1, 8])
    with col_img:
        st.image("escudo.png", width=100)
    with col_tit:
        st.markdown(f"<h1 class='titulo-principal'>GRAN POLLA MUNDIALISTA FÁBRICA DE MONEDA</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitulo'>⚽ Panel Oficial de Resultados y Posiciones en Tiempo Real</p>", unsafe_allow_html=True)
else:
    # Ruta web alternativa directa y optimizada en alta definición (formato PNG transparente)
    url_alternativa = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Escudo_del_Banco_de_la_Rep%C3%BAblica_de_Colombia.svg/512px-Escudo_del_Banco_de_la_Rep%C3%BAblica_de_Colombia.svg.png"
    col_img, col_tit = st.columns([1, 8])
    with col_img:
        st.image(url_alternativa, width=100, output_format="PNG")
    with col_tit:
        st.markdown(f"<h1 class='titulo-principal'>GRAN POLLA MUNDIALISTA FÁBRICA DE MONEDA</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitulo'>⚽ Panel Oficial de Resultados y Posiciones en Tiempo Real</p>", unsafe_allow_html=True)

st.divider()

# ----------------------------------------
# CARGA Y VALIDACIÓN DE DATOS
# ----------------------------------------
ruta_eliminatorias = 'Ranking_General_Acumulado.csv'
ruta_grupos = 'Ranking_Diario_Fase_Grupos.csv'

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
else:
    st.warning("Esperando el procesamiento y carga de los primeros archivos de puntuación...")

# ----------------------------------------
# SECCIÓN DE VISUALIZACIONES COMPARTIDAS
# ----------------------------------------
if df is not None:
    st.markdown(f"#### 📍 Etapa del Torneo: **{fase_actual}**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. EL PODIO (Métricas Superiores)
    col1, col2, col3 = st.columns(3)
    if len(df) >= 1:
        col2.metric("🥇 1er Puesto", df.iloc[0]['Participante'], f"{df.iloc[0][columna_orden]} Puntos")
    if len(df) >= 2:
        col1.metric("🥈 2do Puesto", df.iloc[1]['Participante'], f"{df.iloc[1][columna_orden]} Puntos")
    if len(df) >= 3:
        col3.metric("🥉 3er Puesto", df.iloc[2]['Participante'], f"{df.iloc[2][columna_orden]} Puntos")
        
    st.markdown("<br>", unsafe_allow_html=True)

    # Creamos una estructura de dos columnas para colocar la gráfica y la tabla en paralelo de forma simétrica
    col_grafica, col_tabla = st.columns([1, 1])

    with col_grafica:
        st.markdown("### 📊 Tendencia de Puntuaciones")
        
        # Configuración homogénea de la gráfica utilizando la paleta institucional
        grafica = alt.Chart(df).mark_bar(
            color=COLOR_PRINCIPAL, 
            cornerRadiusTopLeft=5, 
            cornerRadiusTopRight=5
        ).encode(
            x=alt.X('Participante:N', 
                    sort='-y', 
                    axis=alt.Axis(
                        labelAngle=-45, 
                        labelColor=COLOR_TEXTO, 
                        title="Participantes",
                        titleColor=COLOR_PRINCIPAL,
                        labelFontSize=11,
                        grid=False
                    )),
            y=alt.Y(f'{columna_orden}:Q', 
                    axis=alt.Axis(
                        labelColor=COLOR_TEXTO, 
                        title="Puntuación Total",
                        titleColor=COLOR_PRINCIPAL,
                        gridColor="#E2E8F0",
                        labelFontSize=11
                    )),
            tooltip=['Participante', alt.Tooltip(f'{columna_orden}:Q', title='Puntos')]
        ).properties(
            height=380,
            background='transparent'
        )
        st.altair_chart(grafica, use_container_width=True, theme=None)

    with col_tabla:
        st.markdown("### 📋 Tabla de Posiciones Consolidada")
        
        # Estilización homogénea de la tabla para emparejar con el gráfico
        # El puntaje más alto se destaca sutilmente con un tono azul claro institucional
        df_estilizado = df.style.highlight_max(
            subset=[columna_orden], 
            color='#DCE6F1'
        ).format(precision=0)
        
        st.dataframe(
            df_estilizado,
            use_container_width=True,
            hide_index=True,
            height=380
        )
    
    st.divider()
    st.markdown("<p style='text-align: center; color: #8A99AD !important; font-size: 0.85em;'>Cálculos generados de forma automática bajo los parámetros oficiales de la Mesa Técnica.</p>", unsafe_allow_html=True)