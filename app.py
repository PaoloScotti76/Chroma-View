import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Visualizzatore Chromateca con filtro per TEXTURE")

# 🔗 Inserisci qui il link diretto al file CSV su GitHub
csv_url = "https://raw.githubusercontent.com/tuo-utente/tuo-repo/main/Chromateca_database.csv"

try:
    df = pd.read_csv(csv_url, sep=";", engine="python", on_bad_lines="skip")

    if 'TEXTURE' in df.columns:
        texture_options = df['TEXTURE'].dropna().unique()
        selected_textures = st.multiselect("Filtra per TEXTURE", options=sorted(texture_options))

        if selected_textures:
            filtered_df = df[df['TEXTURE'].isin(selected_textures)]
        else:
            filtered_df = df

        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("La colonna 'TEXTURE' non è presente nel file.")
except Exception as e:
    st.error(f"Errore nel caricamento del file CSV: {e}")
