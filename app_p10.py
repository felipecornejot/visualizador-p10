import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests

# --- Paleta de Colores ---
# Definición de colores en formato RGB (0-1) para Matplotlib
color_primario_1_rgb = (14/255, 69/255, 74/255) # 0E454A (Oscuro)
color_primario_2_rgb = (31/255, 255/255, 95/255) # 1FFF5F (Verde vibrante)
color_primario_3_rgb = (255/255, 255/255, 255/255) # FFFFFF (Blanco)

# Colores del logo de Sustrend para complementar
color_sustrend_1_rgb = (0/255, 155/255, 211/255) # 009BD3 (Azul claro)
color_sustrend_2_rgb = (0/255, 140/255, 207/255) # 008CCF (Azul medio)
color_sustrend_3_rgb = (0/255, 54/255, 110/255) # 00366E (Azul oscuro)

# Selección de colores para los gráficos
colors_for_charts = [color_primario_1_rgb, color_primario_2_rgb, color_sustrend_1_rgb, color_sustrend_3_rgb]

# --- Configuración de la página de Streamlit ---
st.set_page_config(layout="wide")

st.title('✨ Visualizador de Impactos - Proyecto P10')
st.subheader('Zero-E: Ganadería Regenerativa')
st.markdown("""
    Ajusta los parámetros para explorar cómo las proyecciones de impacto ambiental y económico del Proyecto
    Zero-E varían con diferentes escenarios. Este proyecto busca reducir significativamente las emisiones
    de gases de efecto invernadero (GEI) en la ganadería, además de disminuir las emisiones de amoniaco y
    ácido sulfhídrico, a través de un aditivo animal natural a partir de extractos de Quillay y otros subproductos.
""")

# --- Widgets Interactivos para Parámetros (Streamlit) ---
st.sidebar.header('Parámetros de Simulación')

animales_beneficiados = st.sidebar.slider(
    'Animales Beneficiados (n°):',
    min_value=50,
    max_value=5000,
    value=1000, # Valor por defecto aumentado para mayor impacto
    step=50,
    help="Número de animales (rumiantes) que se benefician del aditivo anualmente."
)

factor_gei_animal = st.sidebar.slider(
    'Factor de Emisión Entérica (tCO₂e/animal/año):',
    min_value=15.0,
    max_value=25.0,
    value=20.0,
    step=0.5,
    help="Factor promedio de emisión de metano entérico por animal al año."
)

tasa_reduccion = st.sidebar.slider(
    'Tasa de Reducción Esperada de GEI (%):',
    min_value=10.0,
    max_value=40.0,
    value=30.0,
    step=1.0,
    format='%.1f%%',
    help="Porcentaje de reducción de emisiones de GEI logrado por el aditivo."
)

volumen_subproductos = st.sidebar.slider(
    'Volumen de Subproductos Utilizados (ton/año):',
    min_value=5,
    max_value=200,
    value=15, # Mantener el valor de la ficha P10
    step=5,
    help="Volumen anual de subproductos (Quillay, etc.) valorizados como materia prima."
)

porcentaje_valorizacion = st.sidebar.slider(
    'Porcentaje de Valorización de Subproductos (%):',
    min_value=80.0,
    max_value=95.0,
    value=87.0,
    step=1.0,
    format='%.1f%%',
    help="Porcentaje de los subproductos utilizados que se transforma efectivamente en aditivo."
)

sustitucion_aditivos = st.sidebar.slider(
    'Sustitución de Aditivos Sintéticos (%):',
    min_value=10.0,
    max_value=30.0,
    value=15.0,
    step=1.0,
    format='%.1f%%',
    help="Porcentaje de aditivos sintéticos que son reemplazados por el aditivo natural."
)

precio_aditivo = st.sidebar.slider(
    'Precio Aditivo Natural (CLP/ton):',
    min_value=1_000_000,
    max_value=3_000_000,
    value=2_000_000,
    step=100_000,
    help="Precio de venta estimado del aditivo natural por tonelada."
)

# --- Cálculos de Indicadores ---
# Convertir porcentajes a fracciones para los cálculos
tasa_reduccion_frac = tasa_reduccion / 100
porcentaje_valorizacion_frac = porcentaje_valorizacion / 100
sustitucion_aditivos_frac = sustitucion_aditivos / 100

gei_ev = animales_beneficiados * factor_gei_animal * tasa_reduccion_frac
material_valorizado = volumen_subproductos * porcentaje_valorizacion_frac
aditivos_sustituidos = material_valorizado * sustitucion_aditivos_frac # Se asume que el volumen de aditivos sustituidos es una proporción del material valorizado
ingresos_estimados = material_valorizado * precio_aditivo
alianzas_comerciales = 4 # Valor fijo según ficha P10
financiacion_circular = 90_000_000 # CLP, valor fijo según ficha P10

st.header('Resultados Proyectados Anuales:')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="💨 **GEI Evitados**", value=f"{gei_ev:.2f} tCO₂e/año")
    st.caption("Reducción de emisiones de gases de efecto invernadero (metano entérico).")
with col2:
    st.metric(label="♻️ **Material Valorizado**", value=f"{material_valorizado:.2f} ton/año")
    st.caption("Cantidad de subproductos industriales transformados en aditivo.")
with col3:
    st.metric(label="🧪 **Aditivos Sintéticos Sustituidos**", value=f"{aditivos_sustituidos:.2f} ton/año")
    st.caption("Volumen de aditivos químicos convencionales reemplazados.")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(label="💰 **Ingresos Generados**", value=f"CLP {ingresos_estimados:,.0f}")
    st.caption("Estimación de ingresos por la venta del aditivo natural.")
with col5:
    st.metric(label="🤝 **Alianzas Comerciales**", value=f"{alianzas_comerciales}")
    st.caption("Número de alianzas estratégicas establecidas (valor de referencia).")
with col6:
    st.metric(label="🔄 **Financiamiento Circular**", value=f"CLP {financiacion_circular:,.0f}")
    st.caption("Financiamiento asociado directamente a la innovación circular (valor de referencia).")


st.markdown("---")

st.header('📊 Análisis Gráfico de Impactos')

# --- Visualización (Gráficos 2D con Matplotlib) ---
# Datos línea base (según ficha P10 y contexto)
# NOTA: Ajustamos las bases para que reflejen un punto de partida para la "proyección"
# Para GEI evitados, la base es lo que se emitiría sin la solución.
# Para material valorizado e ingresos, la base es lo que se lograría con un nivel mínimo de operación o una referencia inicial.
# Los valores originales de la ficha para GEI y material valorizado son 500 tCO2e y 13 ton.
# El ingreso original de la ficha es 26,000,000 CLP (13 ton * 2,000,000 CLP/ton)

base_gei = 500 # tCO2e/año (valor de referencia de la ficha para "GEI evitados")
base_material = 13 # ton/año (valor de referencia de la ficha para "Material valorizado")
base_ingresos = 26_000_000 # CLP/año (valor de referencia de la ficha para "Ingresos generados")


# Creamos una figura con 3 subplots (2D)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7), facecolor=color_primario_3_rgb)
fig.patch.set_facecolor(color_primario_3_rgb)

# Definición de etiquetas y valores para los gráficos de barras 2D
labels = ['Línea Base', 'Proyección']
bar_width = 0.6
x = np.arange(len(labels))

# --- Gráfico 1: GEI Evitados (tCO₂e/año) ---
gei_values = [base_gei, gei_ev]
bars1 = ax1.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax1.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax1.set_title('GEI Evitados', fontsize=14, color=colors_for_charts[3], pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax1.yaxis.set_tick_params(colors=colors_for_charts[0])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='x', length=0)
# Ajuste dinámico del ylim
max_gei_val = max(gei_values)
ax1.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 10)) # Asegura al menos un margen
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', fontsize=9, color=colors_for_charts[0])

# --- Gráfico 2: Material Valorizado (ton/año) ---
material_values = [base_material, material_valorizado]
bars2 = ax2.bar(x, material_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax2.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[0])
ax2.set_title('Material Valorizado', fontsize=14, color=colors_for_charts[3], pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax2.yaxis.set_tick_params(colors=colors_for_charts[0])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='x', length=0)
# Ajuste dinámico del ylim
max_material_val = max(material_values)
ax2.set_ylim(bottom=0, top=max(max_material_val * 1.15, 1)) # 15% de margen superior o mínimo 1 ton
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', fontsize=9, color=colors_for_charts[0])

# --- Gráfico 3: Ingresos Generados (CLP/año) ---
ingresos_values = [base_ingresos, ingresos_estimados]
bars3 = ax3.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax3.set_ylabel('CLP/año', fontsize=12, color=colors_for_charts[3])
ax3.set_title('Ingresos Generados', fontsize=14, color=colors_for_charts[3], pad=20)
ax3.set_xticks(x)
ax3.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax3.yaxis.set_tick_params(colors=colors_for_charts[0])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.tick_params(axis='x', length=0)
# Ajuste dinámico del ylim
max_ingresos_val = max(ingresos_values)
ax3.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1_000_000)) # 15% de margen superior o mínimo 1M CLP
for bar in bars3:
    yval = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"CLP {yval:,.0f}", ha='center', va='bottom', fontsize=9, color=colors_for_charts[0])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
st.pyplot(fig)

# --- Funcionalidad de descarga de cada gráfico ---
st.markdown("---")
st.subheader("Descargar Gráficos Individualmente")

# Función auxiliar para generar el botón de descarga
def download_button(fig, filename_prefix, key):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button(
        label=f"Descargar {filename_prefix}.png",
        data=buf.getvalue(),
        file_name=f"{filename_prefix}.png",
        mime="image/png",
        key=key
    )

# Crear figuras individuales para cada gráfico para poder descargarlas
# Figura 1: GEI Evitados
fig_gei, ax_gei = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_gei.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax_gei.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax_gei.set_title('GEI Evitados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_gei.set_xticks(x)
ax_gei.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_gei.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_gei.spines['top'].set_visible(False)
ax_gei.spines['right'].set_visible(False)
ax_gei.tick_params(axis='x', length=0)
ax_gei.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 10))
for bar in ax_gei.patches:
    yval = bar.get_height()
    ax_gei.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', fontsize=9, color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_gei, "GEI_Evitados", "download_gei")
plt.close(fig_gei)

# Figura 2: Material Valorizado
fig_material, ax_material = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_material.bar(x, material_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax_material.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[0])
ax_material.set_title('Material Valorizado', fontsize=14, color=colors_for_charts[3], pad=20)
ax_material.set_xticks(x)
ax_material.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_material.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_material.spines['top'].set_visible(False)
ax_material.spines['right'].set_visible(False)
ax_material.tick_params(axis='x', length=0)
ax_material.set_ylim(bottom=0, top=max(max_material_val * 1.15, 1))
for bar in ax_material.patches:
    yval = bar.get_height()
    ax_material.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', fontsize=9, color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_material, "Material_Valorizado", "download_material")
plt.close(fig_material)

# Figura 3: Ingresos Generados
fig_ingresos, ax_ingresos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_ingresos.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax_ingresos.set_ylabel('CLP/año', fontsize=12, color=colors_for_charts[3])
ax_ingresos.set_title('Ingresos Generados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_ingresos.set_xticks(x)
ax_ingresos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_ingresos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_ingresos.spines['top'].set_visible(False)
ax_ingresos.spines['right'].set_visible(False)
ax_ingresos.tick_params(axis='x', length=0)
ax_ingresos.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1_000_000))
for bar in ax_ingresos.patches:
    yval = bar.get_height()
    ax_ingresos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"CLP {yval:,.0f}", ha='center', va='bottom', fontsize=9, color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_ingresos, "Ingresos_Generados", "download_ingresos")
plt.close(fig_ingresos)


st.markdown("---")
st.markdown("### Información Adicional:")
st.markdown(f"- **Estado de Avance y Recomendaciones:** El proyecto se encuentra en una etapa piloto de validación funcional y técnica del aditivo natural. Se han realizado pruebas preliminares con resultados alentadores en la reducción de emisiones de metano entérico y mejora del desempeño animal. Se han establecido alianzas iniciales con centros de investigación, agroindustrias y consorcios ganaderos.")

st.markdown("---")
# Texto de atribución centrado
st.markdown("<div style='text-align: center;'>Visualizador Creado por el equipo Sustrend SpA en el marco del Proyecto TT GREEN Foods</div>", unsafe_allow_html=True)

# Aumentar el espaciado antes de los logos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Mostrar Logos ---
col_logos_left, col_logos_center, col_logos_right = st.columns([1, 2, 1])

with col_logos_center:
    sustrend_logo_url = "https://drive.google.com/uc?id=1vx_znPU2VfdkzeDtl91dlpw_p9mmu4dd"
    ttgreenfoods_logo_url = "https://drive.google.com/uc?id=1uIQZQywjuQJz6Eokkj6dNSpBroJ8tQf8"

    try:
        sustrend_response = requests.get(sustrend_logo_url)
        sustrend_response.raise_for_status()
        sustrend_image = Image.open(BytesIO(sustrend_response.content))

        ttgreenfoods_response = requests.get(ttgreenfoods_logo_url)
        ttgreenfoods_response.raise_for_status()
        ttgreenfoods_image = Image.open(BytesIO(ttgreenfoods_response.content))

        st.image([sustrend_image, ttgreenfoods_image], width=100)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar los logos desde las URLs. Por favor, verifica los enlaces: {e}")
    except Exception as e:
        st.error(f"Error inesperado al procesar las imágenes de los logos: {e}")

st.markdown("<div style='text-align: center; font-size: small; color: gray;'>Viña del Mar, Valparaíso, Chile</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align: center; font-size: smaller; color: gray;'>Versión del Visualizador: 1.0 (Proyecto P10)</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='text-align: center; font-size: x-small; color: lightgray;'>Desarrollado con Streamlit</div>", unsafe_allow_html=True)
