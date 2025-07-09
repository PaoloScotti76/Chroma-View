import streamlit as st
import base64
import re
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Visualizzatore Immagini", layout="wide")
st.title("Visualizzatore di immagini da file base64")

# Legge il file localmente
file_path = "img.txt"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Estrae righe con ID e base64 (formato: ID\t"base64...")
    matches = re.findall(r'(\d+)\t"(/9j/[^"]+)"', content)

    if matches:
        ids = [m[0] for m in matches]
        selected_id = st.selectbox("Seleziona un ID immagine da visualizzare:", ids)

        # Trova la stringa base64 corrispondente
        b64_str = dict(matches)[selected_id]

        try:
            image_data = base64.b64decode(b64_str)
            image = Image.open(BytesIO(image_data))
            st.image(image, caption=f"ID immagine: {selected_id}", use_container_width=True)
        except Exception as e:
            st.error(f"Errore nella visualizzazione dell'immagine ID {selected_id}: {e}")
    else:
        st.warning("Nessuna immagine trovata nel file.")
except FileNotFoundError:
    st.error("Il file 'img 1.txt' non è stato trovato nella directory corrente.")
