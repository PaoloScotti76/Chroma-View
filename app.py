import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Visualizzatore Chromateca con filtro per TEXTURE")

uploaded_file = st.file_uploader("Carica il file CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=";", engine="python", on_bad_lines="skip")

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
else:
    st.info("Carica un file CSV per visualizzarne il contenuto.")
