import streamlit as st
import pandas as pd
import os

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Gran Polla Mundialista",
    page_icon="⚽",
    layout="wide"
)

# ─────────────────────────────────────────────
# PALETA
# ─────────────────────────────────────────────
AZUL      = "#003870"
AZUL_MED  = "#185FA5"
AZUL_CLA  = "#E6F1FB"
DORADO    = "#D4AF37"
DORADO_CLA= "#FFF8DC"
TEXTO     = "#1A2530"
FONDO     = "#F4F6F9"
BORDE     = "#DDE2EA"
VERDE     = "#0F6E56"
VERDE_CLA = "#E1F5EE"
GRIS      = "#EEF0F3"

# ─────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
/* Fondo general */
.stApp {{ background-color: {FONDO}; }}

/* Ocultar menú hamburguesa y footer de Streamlit */
#MainMenu, footer {{ visibility: hidden; }}

/* Tipografía base */
html, body, [class*="css"] {{
    font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    color: {TEXTO};
}}

/* Métricas */
div[data-testid="stMetric"] {{
    background-color: #ffffff !important;
    border: 0.5px solid {BORDE} !important;
    border-radius: 10px;
    padding: 16px 20px;
}}
div[data-testid="stMetricLabel"] p {{
    font-size: .82em !important;
    color: #5A6A85 !important;
    font-weight: 600 !important;
}}
div[data-testid="stMetricValue"] {{
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    color: {AZUL} !important;
}}

/* Divisor */
hr {{ border-color: {BORDE}; margin: 20px 0; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# RUTAS DE ARCHIVOS
# ─────────────────────────────────────────────
RUTA_RANKING_ELIM   = "Ranking_General_Acumulado.csv"
RUTA_RANKING_GRUPOS = "Ranking_Diario_Fase_Grupos.csv"
ARCHIVO_REALES_ELIM = "Resultados_Reales_Eliminatorias.xlsx"
ARCHIVO_REALES_GRP  = "Resultados_Reales_Grupos.xlsx"
IMAGEN_MASCOTA      = "Mascotas2026.png"
IMG_FALLBACK        = ("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/"
                       "Escudo_del_Banco_de_la_Rep%C3%BAblica_de_Colombia.svg/"
                       "512px-Escudo_del_Banco_de_la_Rep%C3%BAblica_de_Colombia.svg.png")


# ─────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────
col_tit, col_logo = st.columns([7, 1])

with col_tit:
    st.markdown(f"""
    <div style='background:{AZUL}; border-radius:12px; padding:20px 28px; margin-bottom:6px'>
        <h1 style='color:#fff; font-size:1.6em; font-weight:800; margin:0; line-height:1.2'>
            Gran Polla Mundialista Callejera
        </h1>
        <p style='color:{DORADO}; margin:5px 0 10px; font-size:.92em; font-weight:400'>
            ⚽ Panel oficial · Resultados y posiciones en tiempo real
        </p>
        <span style='background:{DORADO}; color:{AZUL}; font-size:.75em; font-weight:700;
              padding:4px 14px; border-radius:20px; display:inline-block'>
            FIFA World Cup 2026 · EE.UU / México / Canadá
        </span>
    </div>
    """, unsafe_allow_html=True)

with col_logo:
    if os.path.exists(IMAGEN_MASCOTA):
        st.image(IMAGEN_MASCOTA, width=210)
    else:
        st.image(IMG_FALLBACK, width=210)


# ─────────────────────────────────────────────
# CARGA DE DATOS DE RANKING
# ─────────────────────────────────────────────
df           = None
fase_actual  = ""
col_orden    = ""

if os.path.exists(RUTA_RANKING_ELIM):
    df          = pd.read_csv(RUTA_RANKING_ELIM)
    fase_actual = "Clasificación General — Grupos + Eliminatorias"
    col_orden   = "Total_General"
elif os.path.exists(RUTA_RANKING_GRUPOS):
    df          = pd.read_csv(RUTA_RANKING_GRUPOS)
    fase_actual = "Clasificación — Fase de Grupos"
    col_orden   = "Puntos_Grupos"


# ─────────────────────────────────────────────
# HELPER: badge de etapa
# ─────────────────────────────────────────────
def badge_etapa(texto):
    return f"""
    <div style='display:inline-flex; align-items:center; gap:6px;
         background:{AZUL_CLA}; color:{AZUL}; font-size:.8em; font-weight:600;
         padding:6px 14px; border-radius:6px; border:0.5px solid #B5D4F4;
         margin-bottom:16px'>
        📍 {texto}
    </div>"""


# ─────────────────────────────────────────────
# SECCIÓN PRINCIPAL: PODIO + TABLA + BARRAS
# ─────────────────────────────────────────────
if df is not None and not df.empty:
    df = df.sort_values(by=col_orden, ascending=False).reset_index(drop=True)

    st.markdown(badge_etapa(fase_actual), unsafe_allow_html=True)

    # ── Podio (2° | 1° | 3°) ──────────────────────────────────────────────
    def card_podio(emoji, nombre, pts, bg, borde_color, pts_color):
        return f"""
        <div style='background:{bg}; border:0.5px solid {borde_color}; border-radius:10px;
             padding:16px 12px; text-align:center;'>
            <div style='font-size:2em; margin-bottom:6px'>{emoji}</div>
            <div style='font-size:.9em; font-weight:700; color:{AZUL};
                 white-space:nowrap; overflow:hidden; text-overflow:ellipsis'>{nombre}</div>
            <div style='font-size:1.8em; font-weight:800; color:{pts_color};
                 margin:4px 0 2px'>{pts}</div>
            <div style='font-size:.72em; color:#5A6A85; font-weight:500'>puntos</div>
        </div>"""

    p1 = df.iloc[0] if len(df) > 0 else None
    p2 = df.iloc[1] if len(df) > 1 else None
    p3 = df.iloc[2] if len(df) > 2 else None

    c_plata, c_oro, c_bronce = st.columns(3)

    with c_plata:
        if p2 is not None:
            st.markdown(card_podio(
                "🥈", p2["Participante"], int(p2[col_orden]),
                "#F5F7FA", "#B0B7C3", AZUL_MED
            ), unsafe_allow_html=True)

    with c_oro:
        if p1 is not None:
            st.markdown(card_podio(
                "🥇", p1["Participante"], int(p1[col_orden]),
                DORADO_CLA, DORADO, AZUL
            ), unsafe_allow_html=True)

    with c_bronce:
        if p3 is not None:
            st.markdown(card_podio(
                "🥉", p3["Participante"], int(p3[col_orden]),
                "#FEF3EC", "#CD7F32", "#7A4A1E"
            ), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

    # ── Tabla + Barras ─────────────────────────────────────────────────────
    col_tabla, col_barras = st.columns(2)

    with col_tabla:
        st.markdown(f"""
        <div style='background:#fff; border:0.5px solid {BORDE}; border-radius:10px;
             padding:16px; height:340px; overflow-y:auto'>
            <p style='font-size:.78em; font-weight:700; color:{AZUL};
               text-transform:uppercase; letter-spacing:.06em; margin-bottom:10px'>
                📋 Tabla de posiciones
            </p>
        """, unsafe_allow_html=True)

        # Construir HTML de la tabla
        cols_mostrar = ["Participante", col_orden]
        if "Puntos_Grupos" in df.columns and col_orden != "Puntos_Grupos":
            cols_mostrar = ["Participante", "Puntos_Grupos", col_orden]
        if "Puntos_Eliminatorias" in df.columns:
            cols_mostrar = ["Participante", "Puntos_Grupos", "Puntos_Eliminatorias", col_orden]

        headers_label = {
            "Participante": "Participante",
            "Puntos_Grupos": "Grupos",
            "Puntos_Eliminatorias": "Elim.",
            "Total_General": "Total",
            col_orden: "Puntos"
        }

        th_cells = "".join(
            f"<th style='background:{AZUL};color:#fff;padding:9px 10px;"
            f"font-size:.78em;font-weight:600;text-align:left;"
            f"position:sticky;top:0'>{headers_label.get(c, c)}</th>"
            for c in cols_mostrar
        )

        rows_html = ""
        for i, (_, row) in enumerate(df.iterrows()):
            bg_row = AZUL_CLA if i == 0 else ("#F8F9FB" if i % 2 == 0 else "#fff")
            fw     = "700" if i == 0 else "400"
            medal  = ["🥇","🥈","🥉"][i] if i < 3 else f"{i+1}"
            tds    = ""
            for ci, col in enumerate(cols_mostrar):
                val = row[col]
                if ci == 0:
                    tds += (f"<td style='padding:9px 10px;border-bottom:0.5px solid {BORDE};"
                            f"background:{bg_row};font-weight:{fw};font-size:.82em'>"
                            f"{medal} {val}</td>")
                else:
                    tds += (f"<td style='padding:9px 10px;border-bottom:0.5px solid {BORDE};"
                            f"background:{bg_row};text-align:center'>"
                            f"<span style='background:{AZUL};color:#fff;font-size:.75em;"
                            f"font-weight:700;padding:2px 9px;border-radius:20px'>"
                            f"{int(val)}</span></td>")
            rows_html += f"<tr>{tds}</tr>"

        tabla_html = f"""
        <table style='width:100%;border-collapse:collapse;font-size:.82em'>
            <thead><tr>{th_cells}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>"""

        st.markdown(tabla_html + "</div>", unsafe_allow_html=True)

    with col_barras:
        st.markdown(f"""
        <div style='background:#fff; border:0.5px solid {BORDE}; border-radius:10px;
             padding:16px; height:340px; overflow-y:auto'>
            <p style='font-size:.78em; font-weight:700; color:{AZUL};
               text-transform:uppercase; letter-spacing:.06em; margin-bottom:12px'>
                📊 Puntuaciones
            </p>
        """, unsafe_allow_html=True)

        max_pts = int(df[col_orden].max()) if not df.empty and df[col_orden].max() > 0 else 1
        # Gradiente de azules según posición
        colores_barra = [AZUL, AZUL_MED, "#378ADD", "#85B7EB", "#B5D4F4", "#D0E8F8"]

        barras_html = ""
        for i, (_, row) in enumerate(df.iterrows()):
            nombre  = str(row["Participante"])
            pts     = int(row[col_orden])
            pct     = round(pts / max_pts * 100)
            color   = colores_barra[min(i, len(colores_barra)-1)]
            txt_col = "#fff" if i < 4 else AZUL

            nombre_corto = nombre[:14] + "…" if len(nombre) > 14 else nombre
            barras_html += f"""
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:9px'>
                <span style='font-size:.76em;color:{TEXTO};width:88px;flex-shrink:0;
                      text-align:right;white-space:nowrap;overflow:hidden;
                      text-overflow:ellipsis'>{nombre_corto}</span>
                <div style='flex:1;background:{GRIS};border-radius:20px;
                     height:18px;overflow:hidden'>
                    <div style='width:{pct}%;height:100%;background:{color};
                         border-radius:20px;display:flex;align-items:center;
                         padding-left:7px;font-size:.72em;font-weight:700;
                         color:{txt_col};min-width:24px'>{pts}</div>
                </div>
            </div>"""

        st.markdown(barras_html + "</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER: tarjeta de partido
# ─────────────────────────────────────────────
def tarjeta_partido(local, visita, goles_l, goles_v, avanza=""):
    jugado = goles_l != "-" and goles_v != "-"
    score_bg  = AZUL   if jugado else GRIS
    score_col = "#fff"  if jugado else "#8A9BB0"

    avanza_html = ""
    if avanza:
        avanza_html = f"""
        <div style='margin-top:8px;font-size:.72em;font-weight:700;color:{VERDE};
             background:{VERDE_CLA};padding:3px 8px;border-radius:5px;text-align:center;
             border-top:0.5px solid {BORDE};padding-top:7px'>
            ✅ Avanza: {avanza}
        </div>"""

    return f"""
    <div style='background:#fff;border:0.5px solid {BORDE};border-radius:8px;
         padding:12px;min-width:190px;max-width:240px'>
        <div style='display:flex;justify-content:space-between;
             align-items:center;margin-bottom:5px'>
            <span style='font-size:.83em;font-weight:600;color:{TEXTO}'>{local}</span>
            <span style='background:{score_bg};color:{score_col};font-size:.83em;
                 font-weight:700;padding:2px 10px;border-radius:5px;
                 min-width:26px;text-align:center'>{goles_l}</span>
        </div>
        <div style='display:flex;justify-content:space-between;align-items:center'>
            <span style='font-size:.83em;font-weight:600;color:{TEXTO}'>{visita}</span>
            <span style='background:{score_bg};color:{score_col};font-size:.83em;
                 font-weight:700;padding:2px 10px;border-radius:5px;
                 min-width:26px;text-align:center'>{goles_v}</span>
        </div>
        {avanza_html}
    </div>"""


def seccion_fase(label, icon="⚽"):
    return f"""
    <div style='font-size:.78em;font-weight:700;color:{AZUL};
         text-transform:uppercase;letter-spacing:.08em;
         margin:18px 0 10px;display:flex;align-items:center;gap:6px'>
        {icon} {label}
    </div>"""


# ─────────────────────────────────────────────
# FIXTURE / MARCADORES OFICIALES
# ─────────────────────────────────────────────
st.markdown(f"""
<p style='font-size:.78em;font-weight:700;color:{AZUL};
   text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px'>
    🏟️ Marcadores oficiales y fixture
</p>
""", unsafe_allow_html=True)


# ── ELIMINATORIAS ──────────────────────────────────────────────────────────
if os.path.exists(ARCHIVO_REALES_ELIM):
    df_elim = pd.read_excel(ARCHIVO_REALES_ELIM)
    df_fixture = df_elim.dropna(subset=["Equipo Local", "Equipo Visitante"])

    if not df_fixture.empty:
        fases = df_fixture["Fase"].unique()
        for fase in fases:
            st.markdown(seccion_fase(fase, "🏆"), unsafe_allow_html=True)
            df_fase = df_fixture[df_fixture["Fase"] == fase]

            partidos_html = "<div style='display:flex;flex-wrap:wrap;gap:12px'>"
            for _, row in df_fase.iterrows():
                gl = int(row["Goles L"])  if pd.notna(row.get("Goles L"))  else "-"
                gv = int(row["Goles V"])  if pd.notna(row.get("Goles V"))  else "-"
                av = row["Clasificado a sig. ronda"] if pd.notna(
                    row.get("Clasificado a sig. ronda")) else ""
                partidos_html += tarjeta_partido(
                    row["Equipo Local"], row["Equipo Visitante"], gl, gv, av)
            partidos_html += "</div>"
            st.markdown(partidos_html, unsafe_allow_html=True)
    else:
        st.info("Aún no se han definido las llaves eliminatorias.")


# ── FASE DE GRUPOS ─────────────────────────────────────────────────────────
elif os.path.exists(ARCHIVO_REALES_GRP):
    df_grp = pd.read_excel(ARCHIVO_REALES_GRP)

    # Partidos jugados (con marcador)
    df_jugados   = df_grp.dropna(subset=["Goles L", "Goles V"])
    # Partidos pendientes (sin marcador pero con equipos)
    df_pendientes = df_grp[
        df_grp["Goles L"].isna() &
        df_grp["Equipo Local"].notna()
    ].head(12)  # mostrar los próximos 12

    if not df_jugados.empty:
        grupos = df_jugados["Grupo"].unique()
        for grupo in grupos:
            st.markdown(seccion_fase(f"Grupo {grupo}"), unsafe_allow_html=True)
            df_g = df_jugados[df_jugados["Grupo"] == grupo]

            html = "<div style='display:flex;flex-wrap:wrap;gap:12px'>"
            for _, row in df_g.iterrows():
                html += tarjeta_partido(
                    row["Equipo Local"], row["Equipo Visitante"],
                    int(row["Goles L"]), int(row["Goles V"])
                )
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

    if not df_pendientes.empty:
        st.markdown(seccion_fase("Próximos partidos", "🕐"), unsafe_allow_html=True)
        html = "<div style='display:flex;flex-wrap:wrap;gap:12px'>"
        for _, row in df_pendientes.iterrows():
            html += tarjeta_partido(
                row["Equipo Local"], row["Equipo Visitante"], "-", "-"
            )
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

    if df_jugados.empty and df_pendientes.empty:
        st.info("Aún no hay marcadores registrados. ¡A la espera del partido inaugural!")

else:
    st.info("No se encontró archivo de resultados. Recuerda subirlo al repositorio.")


# ─────────────────────────────────────────────
# PIE DE PÁGINA
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center;font-size:.75em;color:#8A9BB0;
     border-top:0.5px solid {BORDE};padding-top:14px'>
    Gran Polla Mundialista · FIFA World Cup 2026 ·
    Actualizado automáticamente al recargar la página
</div>
""", unsafe_allow_html=True)
