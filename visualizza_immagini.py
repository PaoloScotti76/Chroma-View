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
df = pd.read_csv("img2.txt", sep="\t")

# Titolo
st.title("Visualizzazione immagini")

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
for idx, row in filtered_df.iterrows():
    cols = st.columns([1, 1, 2, 1, 1, 1, 2])
    cols[0].write(row["ID"])
    cols[1].write(row["CODE"])
    cols[2].write(row["GODET_DESC"])
    cols[3].write(row["CUSTOMER"])
    cols[4].write(row["YEAR"])
    cols[5].write(row["GODET"])
    
    img = decode_base64_image(row["IMG"])
    if img:
        cols[6].image(img, caption=f"ID {row['ID']}", use_container_width =True)
    else:
        cols[6].write("Immagine non valida")

