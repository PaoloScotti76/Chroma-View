import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from PIL import Image
import json

# Carica il file JSON dalla stessa cartella dello script
with open("img.json", "r") as f:
    data = json.load(f)

# Converti i dati in DataFrame
df = pd.DataFrame(data)

# Visualizza i dati con immagini decodificate
st.write("Tabella con immagini decodificate:")
for _, row in df.iterrows():
    st.write(f"**ID: {row['ID']}**")
    for col in df.columns:
        if col == "IMG":
            try:
                image_data = base64.b64decode(row[col])
                image = Image.open(BytesIO(image_data))
                st.image(image, caption="IMG", use_column_width=True)
            except Exception as e:
                st.error(f"Errore nella decodifica dell'immagine: {e}")
        else:
            st.write(f"**{col}**: {row[col]}")
    st.markdown("---")
