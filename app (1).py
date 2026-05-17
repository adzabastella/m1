import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================
# CONFIGURATION
# =========================
st.set_page_config(
    page_title="Diamonds Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #020617 0%, #0f172a 25%, #1e3a8a 65%, #312e81 100%);
            background-attachment: fixed;
        }

        .main {
            background: rgba(255,255,255,0.04);
            border-radius: 24px;
            padding: 25px;
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0px 10px 40px rgba(0,0,0,0.35);
        }

        .stMetric {
            background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.05));
            border-radius: 22px;
            padding: 20px;
            box-shadow: 0px 8px 30px rgba(59,130,246,0.25);
            border: 1.5px solid rgba(255,255,255,0.18);
            color: white;
            backdrop-filter: blur(12px);
            transition: 0.3s ease-in-out;
        }

        .stMetric:hover {
            transform: translateY(-4px);
            box-shadow: 0px 12px 35px rgba(96,165,250,0.4);
            border: 1.5px solid rgba(147,197,253,0.5);
        }

        h1, h2, h3 {
            color: #ffffff;
            font-weight: 700;
            text-shadow: 0px 2px 10px rgba(0,0,0,0.35);
        }

        p, label, div, span {
            color: #f8fafc !important;
            font-weight: 500;
        }

        .stMarkdown, .stText {
            color: #f8fafc !important;
        }

        .stSidebar {
            background: rgba(2,6,23,0.95);
        }

        section\[data-testid="stSidebar"\] {
            background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# TITLE
# =========================
st.title("💎 Diamonds Dataset Dashboard")
st.markdown(
    """
    Cette application permet d'explorer les caractéristiques des diamants,
    les tendances de prix et les relations entre les variables.
    """
)

# =========================
# LOAD DATA
# =========================
@st.cache_data

def load_data():
    df = pd.read_csv("diamonds_cleaned.csv")
    return df

try:
    df = load_data()
except:
    st.error("Le fichier 'diamonds_cleaned.csv' est introuvable.")
    st.stop()

# =========================
# SIDEBAR
# =========================
st.sidebar.image("diamant.png", use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;color:white;'>💎 Diamond Analytics</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Filtres")

cut_filter = st.sidebar.multiselect(
    "Qualité de coupe",
    options=sorted(df['cut'].unique()),
    default=sorted(df['cut'].unique())
)

color_filter = st.sidebar.multiselect(
    "Couleur",
    options=sorted(df['color'].unique()),
    default=sorted(df['color'].unique())
)

clarity_filter = st.sidebar.multiselect(
    "Pureté",
    options=sorted(df['clarity'].unique()),
    default=sorted(df['clarity'].unique())
)

price_range = st.sidebar.slider(
    "Intervalle de prix",
    int(df['price'].min()),
    int(df['price'].max()),
    (
        int(df['price'].min()),
        int(df['price'].max())
    )
)

# =========================
# FILTER DATA
# =========================
filtered_df = df[
    (df['cut'].isin(cut_filter)) &
    (df['color'].isin(color_filter)) &
    (df['clarity'].isin(clarity_filter)) &
    (df['price'] >= price_range[0]) &
    (df['price'] <= price_range[1])
]

# =========================
# INSIGHTS BANNER
# =========================
max_price_diamond = filtered_df.loc[filtered_df['price'].idxmax()]
most_common_cut = filtered_df['cut'].mode()[0]

st.markdown(
    f"""
    <div style='background:linear-gradient(90deg, rgba(59,130,246,0.25), rgba(168,85,247,0.25));
                padding:22px;
                border-radius:22px;
                border:1px solid rgba(255,255,255,0.12);
                margin-bottom:25px;
                box-shadow:0px 8px 30px rgba(0,0,0,0.25);'>
        <h2 style='color:white;'>📌 Dashboard Insights</h2>
        <p style='font-size:18px;'>
            💎 Le diamant le plus cher coûte <b>${max_price_diamond['price']:,.0f}</b> avec un poids de <b>{max_price_diamond['carat']:.2f} carats</b>.<br>
            ⭐ La qualité de coupe la plus fréquente est <b>{most_common_cut}</b>.<br>
            📈 Le dashboard met en évidence les relations entre prix, carat, pureté et dimensions.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# KPIs
# =========================
st.subheader("📊 Indicateurs clés")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Nombre de diamants",
        f"{filtered_df.shape[0]:,}"
    )

with col2:
    st.metric(
        "Prix moyen",
        f"${filtered_df['price'].mean():,.0f}"
    )

with col3:
    st.metric(
        "Carat moyen",
        f"{filtered_df['carat'].mean():.2f}"
    )

with col4:
    st.metric(
        "Prix maximum",
        f"${filtered_df['price'].max():,.0f}"
    )

# =========================
# DATA PREVIEW
# =========================
with st.expander("👁️ Aperçu du dataset"):
    st.dataframe(filtered_df.head(20), use_container_width=True)

# =========================
# DISTRIBUTION DU PRIX
# =========================
st.subheader("💰 Distribution des prix")

fig_price = px.histogram(
    filtered_df,
    x='price',
    nbins=50,
    title='Distribution des prix des diamants',
    marginal='box'
)

fig_price.update_layout(
    template='plotly_white',
    height=500
)

st.plotly_chart(fig_price, use_container_width=True)

# =========================
# CARAT VS PRICE
# =========================
st.subheader("💎 Relation entre Carat et Prix")

fig_scatter = px.scatter(
    filtered_df,
    x='carat',
    y='price',
    color='cut',
    size='depth',
    hover_data=['color', 'clarity'],
    title='Carat vs Prix'
)

fig_scatter.update_layout(
    template='plotly_white',
    height=650
)

st.plotly_chart(fig_scatter, use_container_width=True)

# =========================
# PRICE EVOLUTION STYLE AREA
# =========================
st.subheader("🚀 Répartition cumulative des prix")

sorted_prices = filtered_df.sort_values(by='price').reset_index(drop=True)
sorted_prices['index'] = sorted_prices.index

fig_area = px.area(
    sorted_prices,
    x='index',
    y='price',
    title='Croissance cumulative des prix des diamants'
)

fig_area.update_layout(
    template='plotly_dark',
    height=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig_area, use_container_width=True)

# =========================
# ANALYSE CATEGORIELLE
# =========================
st.subheader("📦 Analyse des variables catégorielles")

col5, col6 = st.columns(2)

with col5:
    cut_avg = filtered_df.groupby('cut')['price'].mean().reset_index()

    fig_cut = px.bar(
        cut_avg,
        x='cut',
        y='price',
        color='cut',
        title='Prix moyen par qualité de coupe'
    )

    fig_cut.update_layout(
        template='plotly_white',
        showlegend=False,
        height=500
    )

    st.plotly_chart(fig_cut, use_container_width=True)

with col6:
    clarity_avg = filtered_df.groupby('clarity')['price'].mean().reset_index()

    fig_clarity = px.bar(
        clarity_avg,
        x='clarity',
        y='price',
        color='clarity',
        title='Prix moyen par pureté'
    )

    fig_clarity.update_layout(
        template='plotly_white',
        showlegend=False,
        height=500
    )

    st.plotly_chart(fig_clarity, use_container_width=True)

# =========================
# BOXPLOTS
# =========================
st.subheader("📈 Analyse des outliers")

col7, col8 = st.columns(2)

with col7:
    fig_box_price = px.box(
        filtered_df,
        y='price',
        color='cut',
        title='Outliers du prix selon la coupe'
    )

    fig_box_price.update_layout(
        template='plotly_white',
        height=500
    )

    st.plotly_chart(fig_box_price, use_container_width=True)

with col8:
    fig_box_carat = px.box(
        filtered_df,
        y='carat',
        color='color',
        title='Outliers du carat selon la couleur'
    )

    fig_box_carat.update_layout(
        template='plotly_white',
        height=500
    )

    st.plotly_chart(fig_box_carat, use_container_width=True)

# =========================
# CORRELATION MATRIX
# =========================
st.subheader("🧠 Matrice de corrélation")

numeric_df = filtered_df.select_dtypes(include=np.number)

corr = numeric_df.corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    aspect='auto',
    color_continuous_scale='Blues',
    title='Corrélation entre les variables numériques'
)

fig_corr.update_layout(
    template='plotly_white',
    height=700
)

st.plotly_chart(fig_corr, use_container_width=True)

# =========================
# RADAR CHART
# =========================
st.subheader("🧭 Profil moyen des diamants")

radar_values = [
    filtered_df['carat'].mean(),
    filtered_df['depth'].mean(),
    filtered_df['table'].mean(),
    filtered_df['x'].mean(),
    filtered_df['y'].mean(),
    filtered_df['z'].mean()
]

categories = ['Carat', 'Depth', 'Table', 'X', 'Y', 'Z']

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=radar_values,
    theta=categories,
    fill='toself',
    name='Profil moyen'
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    template='plotly_dark',
    height=550,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig_radar, use_container_width=True)

# =========================
# DIMENSIONS ANALYSIS
# =========================
st.subheader("📐 Analyse des dimensions")

fig_dim = make_subplots(
    rows=1,
    cols=3,
    subplot_titles=('Longueur (x)', 'Largeur (y)', 'Profondeur (z)')
)

fig_dim.add_trace(
    go.Histogram(x=filtered_df['x'], name='x'),
    row=1,
    col=1
)

fig_dim.add_trace(
    go.Histogram(x=filtered_df['y'], name='y'),
    row=1,
    col=2
)

fig_dim.add_trace(
    go.Histogram(x=filtered_df['z'], name='z'),
    row=1,
    col=3
)

fig_dim.update_layout(
    template='plotly_white',
    height=450,
    showlegend=False
)

st.plotly_chart(fig_dim, use_container_width=True)

# =========================
# TOP EXPENSIVE DIAMONDS
# =========================
st.subheader("🏆 Top 10 des diamants les plus chers")

top10 = filtered_df.sort_values(by='price', ascending=False).head(10)

st.dataframe(
    top10[[
        'carat',
        'cut',
        'color',
        'clarity',
        'price'
    ]],
    use_container_width=True
)

# =========================
# DOWNLOAD SECTION
# =========================
st.subheader("📥 Télécharger les données filtrées")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label='Télécharger le dataset filtré',
    data=csv,
    file_name='diamonds_filtered.csv',
    mime='text/csv'
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    """
    <center>
        <h4>💎 Professional Diamonds Dashboard</h4>
        <p>Développé par EBANGA MBALLA</p>
    </center>
    """,
    unsafe_allow_html=True
)
