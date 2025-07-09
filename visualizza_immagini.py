import streamlit as st
import base64
import re
from io import BytesIO
from PIL import Image

st.title("Visualizzatore di immagini da file base64")

uploaded_file = st.file_uploader("Carica un file .txt con immagini JPEG codificate in base64", type="txt")

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")

    # Estrai tutte le stringhe base64 che iniziano con /9j/ (tipico delle immagini JPEG)
    base64_images = re.findall(r'(/9j/[^\\"]+)', content)

    if base64_images:
        st.success(f"Trovate {len(base64_images)} immagini.")
        for i, b64_str in enumerate(base64_images):
            try:
                image_data = base64.b64decode(b64_str)
                image = Image.open(BytesIO(image_data))
                st.image(image, caption=f"Immagine {i+1}", use_column_width=True)
            except Exception as e:
                st.warning(f"Errore nella visualizzazione dell'immagine {i+1}: {e}")
    else:
        st.error("Nessuna immagine base64 trovata nel file.")
