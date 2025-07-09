import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from PIL import Image

# Funzione per convertire base64 in immagine
def decode_base64_image(b64_string):
    try:
        image_data = base64.b64decode(b64_string)
        return Image.open(BytesIO(image_data))
    except Exception:
        return None

# Carica il file TSV
df = pd.read_csv("img.txt", sep="\t")

# Titolo
st.title("Visualizzazione immagini da file TSV")

# Filtri nella barra laterale
st.sidebar.header("Filtri")
id_options = st.sidebar.multiselect("Filtra per ID", options=sorted(df["ID"].unique()))
code_options = st.sidebar.multiselect("Filtra per CODE", options=sorted(df["CODE"].unique()))
godet_options = st.sidebar.multiselect("Filtra per GODET", options=sorted(df["GODET"].unique()))
year_options = st.sidebar.multiselect("Filtra per YEAR", options=sorted(df["YEAR"].unique()))

# Applica i filtri
filtered_df = df.copy()
if id_options:
    filtered_df = filtered_df[filtered_df["ID"].isin(id_options)]
if code_options:
    filtered_df = filtered_df[filtered_df["CODE"].isin(code_options)]
if godet_options:
    filtered_df = filtered_df[filtered_df["GODET"].isin(godet_options)]
if year_options:
    filtered_df = filtered_df[filtered_df["YEAR"].isin(year_options)]

# Visualizza la tabella con immagini
st.markdown("### Risultati filtrati")
for idx, row in filtered_df.iterrows():
    cols = st.columns([1.2, 1.2, 2.5, 1.5, 1.2, 1.2, 3])
    cols[0].markdown(f"<div style='white-space: nowrap'>{row['ID']}</div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div style='white-space: nowrap'>{row['CODE']}</div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div style='white-space: nowrap'>{row['GODET_DESC']}</div>", unsafe_allow_html=True)
    cols[3].markdown(f"<div style='white-space: nowrap'>{row['CUSTOMER']}</div>", unsafe_allow_html=True)
    cols[4].markdown(f"<div style='white-space: nowrap'>{row['YEAR']}</div>", unsafe_allow_html=True)
