import streamlit as st
import base64
import re
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Visualizzatore Immagini", layout="wide")
st.title("Visualizzatore di immagini da file base64")

file_path = "img.txt"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Estrai coppie ID e stringhe base64
    matches = re.findall(r'(\d+)\t"(/9j/[^\\"]+)"', content)

    if matches:
        id_options = ["Tutti"] + [m[0] for m in matches]
        selected_id = st.selectbox("Seleziona un ID da visualizzare:", id_options)

        if selected_id == "Tutti":
            for img_id, b64_str in matches:
                try:
                    image_data = base64.b64decode(b64_str)
                    image = Image.open(BytesIO(image_data))
                    st.image(image, caption=f"ID: {img_id}", width=200)
                except Exception as e:
                    st.warning(f"Errore con immagine ID {img_id}: {e}")
        else:
            b64_str = dict(matches).get(selected_id)
            if b64_str:
                try:
                    image_data = base64.b64decode(b64_str)
                    image = Image.open(BytesIO(image_data))
                    st.image(image, caption=f"ID: {selected_id}", width=200)
                except Exception as e:
                    st.error(f"Errore nella visualizzazione dell'immagine ID {selected_id}: {e}")
    else:
        st.warning("Nessuna immagine trovata nel file.")
except FileNotFoundError:
    st.error("Il file 'img 1.txt' non è stato trovato nella directory corrente.")
