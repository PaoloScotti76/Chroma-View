import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from PIL import Image

# Carica il file TSV
df = pd.read_csv("img.txt", sep="\t")

# Funzione per convertire base64 in immagine
def decode_base64_image(b64_string):
    try:
        image_data = base64.b64decode(b64_string)
        return Image.open(BytesIO(image_data))
    except Exception as e:
        return None

# Titolo
st.title("Visualizzazione immagini da file TSV")

# Visualizza la tabella con immagini
for idx, row in df.iterrows():
    cols = st.columns([1, 1, 2, 1, 1, 1, 2])
    cols[0].write(row["ID"])
    cols[1].write(row["CODE"])
    cols[2].write(row["GODET_DESC"])
    cols[3].write(row["CUSTOMER"])
    cols[4].write(row["YEAR"])
    cols[5].write(row["GODET"])
    
    img = decode_base64_image(row["IMG"])
    if img:
        cols[6].image(img, caption=f"ID {row['ID']}", use_column_width=True)
    else:
        cols[6].write("Immagine non valida")
