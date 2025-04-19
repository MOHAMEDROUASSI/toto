import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analyse de données", layout="wide")

# Titre de l'application
st.title("📊 Application d'analyse de données avec Streamlit")

# Upload du fichier CSV
uploaded_file = st.file_uploader("📁 Importer un fichier CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Aperçu des données")
    st.dataframe(df.head())

    # Choisir une colonne pour filtrer
    colonnes = df.select_dtypes(include='object').columns.tolist()
    if colonnes:
        col_filtre = st.selectbox("🔍 Filtrer selon une colonne :", colonnes)
        valeurs_uniques = df[col_filtre].dropna().unique()
        valeur = st.multiselect(f"Valeurs de {col_filtre} :", valeurs_uniques)

        if valeur:
            df = df[df[col_filtre].isin(valeur)]
            st.success(f"{len(df)} lignes affichées après filtre")

    st.subheader("📈 Statistiques descriptives")
    st.write(df.describe())

    # Graphique simple
    colonnes_numeriques = df.select_dtypes(include='number').columns.tolist()
    if colonnes_numeriques:
        col_graph = st.selectbox("📊 Choisir une colonne numérique à tracer :", colonnes_numeriques)
        fig, ax = plt.subplots()
        df[col_graph].hist(bins=20, color="skyblue", edgecolor="black", ax=ax)
        st.pyplot(fig)

    # Export CSV
    st.subheader("📤 Exporter les données filtrées")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger CSV",
        data=csv,
        file_name='données_filtrées.csv',
        mime='text/csv'
    )

else:
    st.info("📝 Veuillez importer un fichier CSV pour commencer.")
