import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from PIL import Image
import requests
import json

# URL del file JSON su GitHub
GITHUB_URL = "https://raw.githubusercontent.com/PaoloScotti76/Chroma-View/main/img.json"

@st.cache_data
def load_data(url):
    response = requests.get(url)
    data = json.loads(response.text)
    return pd.DataFrame(data)

# Carica i dati
df = load_data(GITHUB_URL)

# Filtro multiselezione
selected_ids = st.sidebar.multiselect("Seleziona ID", df["ID"].unique(), default=df["ID"].unique())

# Filtra il DataFrame
filtered_df = df[df["ID"].isin(selected_ids)]

# Visualizza tutte le colonne
st.title("Visualizzatore dati e immagini")
st.dataframe(filtered_df)

# Visualizza le immagini dalla colonna IMG
for _, row in filtered_df.iterrows():
    st.subheader(f"ID: {row['ID']}")
    try:
        image_data = base64.b64decode(row["IMG"])
        image = Image.open(BytesIO(image_data))
        st.image(image, caption=f"Immagine per ID {row['ID']}", use_column_width=True)
    except Exception as e:
        st.error(f"Errore nel caricamento immagine per ID {row['ID']}: {e}")
