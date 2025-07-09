import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from PIL import Image

st.title("Visualizzatore immagini da file JSON")

uploaded_file = st.file_uploader("Carica il file img.json", type="json")

if uploaded_file is not None:
    try:
        # Carica il contenuto JSON
        data = pd.read_json(uploaded_file)

        # Mostra le colonne presenti
        st.subheader("Colonne presenti nel file:")
        st.write(data.columns.tolist())

        # Selezione multipla degli ID
        if "ID" in data.columns:
            selected_ids = st.multiselect("Seleziona uno o più ID:", data["ID"].unique())

            # Filtra il DataFrame in base agli ID selezionati
            filtered_data = data[data["ID"].isin(selected_ids)]

            # Visualizza le immagini codificate in base64
            for _, row in filtered_data.iterrows():
                st.markdown(f"**ID:** {row['ID']}")
                if "IMG" in row and isinstance(row["IMG"], str):
                    try:
                        img_data = base64.b64decode(row["IMG"])
                        image = Image.open(BytesIO(img_data))
                        st.image(image, caption=f"ID: {row['ID']}", use_column_width=True)
                    except Exception as e:
                        st.error(f"Errore nella decodifica dell'immagine per ID {row['ID']}: {e}")
        else:
            st.warning("La colonna 'ID' non è presente nel file.")
    except Exception as e:
        st.error(f"Errore nella lettura del file JSON: {e}")
else:
    st.info("Carica un file JSON per iniziare.")
