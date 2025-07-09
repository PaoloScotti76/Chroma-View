import streamlit as st
import pandas as pd
import base64
from io import StringIO
from PIL import Image
import io

st.title("Visualizzatore di immagini base64 da ID")

# Caricamento del file
uploaded_file = st.file_uploader("Carica il file .txt", type="txt")

if uploaded_file is not None:
    # Leggi il contenuto come testo
    content = uploaded_file.read().decode("utf-8")

    # Parsing manuale: rimuovi intestazioni e righe vuote
    lines = [line for line in content.splitlines() if line.strip()]
    header = lines[0].replace('"', '').split('\t')
    data = [line.replace('"', '').split('\t') for line in lines[1:] if len(line.split('\t')) == len(header)]

    # Crea DataFrame
    df = pd.DataFrame(data, columns=header)

    # Filtro per ID
    ids = df["ID"].unique()
    selected_ids = st.multiselect("Seleziona uno o più ID", ids)

    if selected_ids:
        filtered_df = df[df["ID"].isin(selected_ids)]

        for idx, row in filtered_df.iterrows():
            st.markdown(f"**ID:** {row['ID']} - **CODE:** {row['CODE']}")
            try:
                img_data = base64.b64decode(row["IMG"])
                image = Image.open(io.BytesIO(img_data))
                st.image(image, caption=f"Immagine per ID {row['ID']}", use_column_width=True)
            except Exception as e:
                st.error(f"Errore nel caricamento dell'immagine per ID {row['ID']}: {e}")
