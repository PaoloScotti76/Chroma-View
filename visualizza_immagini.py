import streamlit as st
import pandas as pd
import base64
import re
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Visualizzatore Immagini con Metadati", layout="wide")
st.title("Visualizzatore immagini")

# Leggi il file
file_path = "img2.txt"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Estrai righe con ID e metadati
    pattern = r'(\d+)\t"([^"]+)"\t"([^"]+)"\t"([^"]+)"\t"([^"]+)"\t"([^"]+)"\t"([^"]+)"\t"(/9j/[^"]+)"'
    matches = re.findall(pattern, content)

    if matches:
        data = pd.DataFrame(matches, columns=["ID", "CODE", "GODET_DESC", "CUSTOMER", "YEAR", "GODET", "NOTE", "IMG"])
        id_options = ["Tutti"] + sorted(data["ID"].unique().tolist())
        selected_id = st.selectbox("Seleziona un ID da visualizzare:", id_options)

        if selected_id == "Tutti":
            for _, row in data.iterrows():
                try:
                    image_data = base64.b64decode(row["IMG"])
                    image = Image.open(BytesIO(image_data))
                    st.image(image, caption=f"ID: {row['ID']} - {row['CODE']}", width=200)
                except Exception as e:
                    st.warning(f"Errore con immagine ID {row['ID']}: {e}")
        else:
            row = data[data["ID"] == selected_id].iloc[0]
            try:
                image_data = base64.b64decode(row["IMG"])
                image = Image.open(BytesIO(image_data))
                st.image(image, caption=f"ID: {row['ID']} - {row['CODE']}", width=200)
                st.markdown(f"""
                **CODE**: {row['CODE']}  
                **GODET_DESC**: {row['GODET_DESC']}  
                **CUSTOMER**: {row['CUSTOMER']}  
                **YEAR**: {row['YEAR']}  
                **GODET**: {row['GODET']}  
                **NOTE**: {row['NOTE']}
                """)
            except Exception as e:
                st.error(f"Errore nella visualizzazione dell'immagine ID {selected_id}: {e}")
    else:
        st.warning("Nessuna immagine trovata nel file.")
except File
