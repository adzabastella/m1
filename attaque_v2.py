import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analyse Cardiaque", layout="wide", page_icon="❤️")

# Style personnalisé
st.markdown("""
<style>
    /* En-tête principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* Cartes métriques */
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    /* Sidebar colorée */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Chargement des données
@st.cache_data 
def load_data():
    df = pd.read_csv("attaque_cardiaque.csv") 
    
    # Supprime les espaces et caractères invisibles des noms de colonnes
    df.columns = df.columns.str.strip()
    df['DEATH_EVENT'] = df['DEATH_EVENT'].astype(int)
    
    return df
df = load_data()
# Menu stylisé
st.sidebar.markdown("#  Menu Principal")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "",
    ["🏠 Accueil", "📊 Statistiques", "📈 Visualisations", "🔍 Comparaison"],
    format_func=lambda x: f"**{x}**"
)

# Accueil
if menu == "🏠 Accueil":
    st.markdown("""
    <div class="main-header">
        <h1>❤️ Analyse des facteurs de risque cardiaque</h1>
        <p>Exploration interactive du dataset sur l'insuffisance cardiaque</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métriques colorées
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Patients</h3>
            <h2>{len(df)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <h3> Variables</h3>
            <h2>{len(df.columns)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: #333;">
            <h3>💀 Décès</h3>
            <h2>{df['DEATH_EVENT'].sum()}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); color: #333;">
            <h3>📈 Mortalité</h3>
            <h2>{df['DEATH_EVENT'].mean()*100:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(" Variables principales")
        st.markdown("""
        - **age** : Âge du patient
        - **ejection_fraction** : Fraction d'éjection (%)
        - **serum_creatinine** : Créatinine sérique
        - **time** : Temps de suivi (jours)
        - **DEATH_EVENT** : Décès (0=Vivant, 1=Décédé)
        """)
    
    with col2:
        # Mini graphique de survie
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#2ecc71', '#e74c3c']
        df['DEATH_EVENT'].value_counts().plot(kind='pie', autopct='%1.1f%%', 
                                                colors=colors, ax=ax, shadow=True)
        ax.set_title("Répartition Vivants vs Décédés", fontsize=14)
        ax.set_ylabel("")
        st.pyplot(fig)
    
    st.info(" **Utilisez le menu à gauche** pour explorer les données en détail")

# statistiques
elif menu == "📊 Statistiques":
    st.markdown("## 📊 Statistiques descriptives")
    st.markdown("---")
    
    # Aperçu des données
    st.subheader("🔍 Aperçu des données")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Statistiques
    st.subheader("📈 Résumé statistique")
    st.dataframe(df.describe().style.background_gradient(cmap='Blues'), use_container_width=True)
    
    # Infos générales
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📏 Dimensions")
        st.write(f"**Lignes :** {df.shape[0]}")
        st.write(f"**Colonnes :** {df.shape[1]}")
    
    with col2:
        st.subheader("🔧 Types de données")
        st.dataframe(df.dtypes.astype(str).to_frame("Type"), use_container_width=True)
    
    # Valeurs manquantes
    st.subheader("✅ Qualité des données")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        st.success("🎉 **Aucune valeur manquante** - Base de données propre !")
    else:
        st.warning(f"⚠️ {missing.sum()} valeurs manquantes détectées")

# visualisations
elif menu == "📈 Visualisations":
    st.markdown("## 📈 Distribution des variables")
    st.markdown("---")
    
    # Variables numériques
    vars_num = ['age', 'ejection_fraction', 'serum_creatinine', 'time', 
                'creatinine_phosphokinase', 'platelets', 'serum_sodium']
    
    noms_fr = {
        'age': 'Âge', 'ejection_fraction': 'Fraction d\'éjection',
        'serum_creatinine': 'Créatinine', 'time': 'Temps de suivi',
        'creatinine_phosphokinase': 'CPK', 'platelets': 'Plaquettes',
        'serum_sodium': 'Sodium'
    }
    
    col1, col2 = st.columns([1, 3])
    with col1:
        choix = st.selectbox("Choisissez une variable :", vars_num, format_func=lambda x: noms_fr[x])
        show_kde = st.checkbox("Afficher la courbe", value=True)
        st.markdown("---")
        st.markdown(f"**Statistiques de {noms_fr[choix]} :**")
        st.write(f"- Moyenne : **{df[choix].mean():.2f}**")
        st.write(f"- Médiane : **{df[choix].median():.2f}**")
        st.write(f"- Min / Max : **{df[choix].min():.2f}** / **{df[choix].max():.2f}**")
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df[choix], bins=30, kde=show_kde, color='#667eea', ax=ax)
        ax.set_title(f"Distribution de {noms_fr[choix]}", fontsize=14, fontweight='bold')
        ax.set_xlabel(noms_fr[choix])
        ax.set_ylabel("Fréquence")
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('#f8f9fa')
        st.pyplot(fig)
    
    # Variables binaires
    st.markdown("---")
    st.subheader("📊 Variables catégorielles")
    
    vars_bin = ['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking']
    noms_bin = {'anaemia': 'Anémie', 'diabetes': 'Diabète', 
                'high_blood_pressure': 'Hypertension',
                'sex': 'Sexe', 'smoking': 'Tabagisme'}
    labels_bin = {'anaemia': ['Non', 'Oui'], 'diabetes': ['Non', 'Oui'],
                  'high_blood_pressure': ['Non', 'Oui'], 'sex': ['Femme', 'Homme'],
                  'smoking': ['Non', 'Oui']}
    
    cols = st.columns(3)
    for i, var in enumerate(vars_bin):
        with cols[i % 3]:
            fig, ax = plt.subplots(figsize=(5, 4))
            counts = df[var].value_counts()
            colors = ['#2ecc71', '#e74c3c']
            counts.plot(kind='bar', ax=ax, color=colors)
            ax.set_title(noms_bin[var], fontsize=12, fontweight='bold')
            ax.set_xlabel("")
            ax.set_ylabel("Nombre")
            ax.set_xticklabels(labels_bin[var], rotation=0)
            for j, v in enumerate(counts):
                ax.text(j, v + 5, str(v), ha='center', fontweight='bold')
            st.pyplot(fig)

# comparaison
elif menu == " Comparaison":
    st.markdown("##  Vivants vs Décédés")
    st.markdown("---")
    
    vars_num = ['age', 'ejection_fraction', 'serum_creatinine', 'time', 
                'creatinine_phosphokinase', 'platelets', 'serum_sodium']
    
    noms_fr = {
        'age': 'Âge', 'ejection_fraction': 'Fraction d\'éjection',
        'serum_creatinine': 'Créatinine', 'time': 'Temps de suivi',
        'creatinine_phosphokinase': 'CPK', 'platelets': 'Plaquettes',
        'serum_sodium': 'Sodium'
    }
    
    choix = st.selectbox("Variable à comparer :", vars_num, format_func=lambda x: noms_fr[x])
    
    # Boxplot coloré
    fig, ax = plt.subplots(figsize=(10, 6))
    bp = sns.boxplot(x='DEATH_EVENT', y=choix, data=df, ax=ax)
    
    for i, patch in enumerate(ax.artists):
        patch.set_facecolor('#2ecc71' if i == 0 else '#e74c3c')
        patch.set_alpha(0.7)
    
    ax.set_xticklabels(['🟢 Vivant', '🔴 Décédé'])
    ax.set_title(f"Distribution de {noms_fr[choix]} selon le statut", fontsize=14, fontweight='bold')
    ax.set_ylabel(noms_fr[choix])
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('#f8f9fa')
    st.pyplot(fig)
    
    # Statistiques comparatives
    st.subheader("📊 Comparaison des moyennes")
    
    vivants = df[df['DEATH_EVENT'] == 0][choix]
    decedes = df[df['DEATH_EVENT'] == 1][choix]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: #2ecc71; padding: 1rem; border-radius: 15px; color: white; text-align: center;">
            <h4>🟢 Vivants</h4>
            <h3>{vivants.mean():.2f}</h3>
            <small>(n={len(vivants)})</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #e74c3c; padding: 1rem; border-radius: 15px; color: white; text-align: center;">
            <h4>🔴 Décédés</h4>
            <h3>{decedes.mean():.2f}</h3>
            <small>(n={len(decedes)})</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        diff = decedes.mean() - vivants.mean()
        color = "#e74c3c" if diff > 0 else "#2ecc71"
        st.markdown(f"""
        <div style="background: {color}; padding: 1rem; border-radius: 15px; color: white; text-align: center;">
            <h4> Différence</h4>
            <h3>{diff:+.2f}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Taux de mortalité par catégorie
    st.markdown("---")
    st.subheader("📊 Taux de mortalité par catégorie")
    
    vars_bin = ['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking']
    noms_bin = {'anaemia': 'Anémie', 'diabetes': 'Diabète', 
                'high_blood_pressure': 'Hypertension',
                'sex': 'Sexe', 'smoking': 'Tabagisme'}
    
    choix_cat = st.selectbox("Catégorie :", vars_bin, format_func=lambda x: noms_bin[x])
    
    taux = df.groupby(choix_cat)['DEATH_EVENT'].mean() * 100
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(range(len(taux)), taux.values, color=['#3498db', '#e74c3c'])
    ax.set_title(f"Taux de mortalité selon {noms_bin[choix_cat]}", fontsize=14, fontweight='bold')
    ax.set_ylabel("Taux de mortalité (%)")
    ax.set_xticks(range(len(taux)))
    ax.set_xticklabels(['Non', 'Oui'] if choix_cat != 'sex' else ['Femme', 'Homme'])
    ax.set_ylim(0, 60)
    
    for bar, v in zip(bars, taux.values):
        ax.text(bar.get_x() + bar.get_width()/2, v + 2, f"{v:.1f}%", ha='center', fontweight='bold')
    
    st.pyplot(fig)

# Sidebar info stylisée
st.sidebar.markdown(f"""
<div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
    <small>📊 Dataset : {len(df)} patients<br>
    ❤️ Décès : {df['DEATH_EVENT'].sum()} ({df['DEATH_EVENT'].mean()*100:.0f}%)<br>
    🛠️ Built with Streamlit</small>
</div>
""", unsafe_allow_html=True)
