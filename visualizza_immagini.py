import streamlit as st
import pandas as pd
import requests
import base64
from io import BytesIO
from PIL import Image

# URL del file JSON su GitHub
GITHUB_URL = "img.json"

@st.cache_data
def load_data(url):
    response = requests.get(url)
    text = response.text
    records = []
    for block in text.split("id "):
        if "<BASE64>" in block:
            try:
                id_part = block.split()[0]
                base64_data = block.split("<BASE64>")[1].split("</BASE64>")[0].strip()
                records.append({"ID": id_part, "IMG": base64_data})
            except Exception:
                continue
    return pd.DataFrame(records)

# Carica i dati
df = load_data(GITHUB_URL)

# Filtro multiselezione
selected_ids = st.sidebar.multiselect("Seleziona ID", df["ID"].unique(), default=df["ID"].unique())

# Filtra il DataFrame
filtered_df = df[df["ID"].isin(selected_ids)]

# Visualizza le immagini
st.title("Visualizzatore immagini da JSON")

for _, row in filtered_df.iterrows():
    st.subheader(f"ID: {row['ID']}")
    try:
        image_data = base64.b64decode(row["IMG"])
        image = Image.open(BytesIO(image_data))
        st.image(image, caption=f"Immagine per ID {row['ID']}", use_column_width=True)
    except Exception as e:
        st.error(f"Errore nel caricamento immagine per ID {row['ID']}: {e}")
