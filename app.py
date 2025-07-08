import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Visualizzatore Chromateca")

uploaded_file = st.file_uploader("Carica un file CSV", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=";", engine="python", on_bad_lines="skip")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Errore durante la lettura del file: {e}")
else:
    st.info("Carica un file CSV per visualizzarne il contenuto.")