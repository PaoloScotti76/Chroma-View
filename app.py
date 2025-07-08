import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Visualizzatore Chromateca con filtro TEXTURE e LED ST_STABILITY")

# URL del file CSV su GitHub
csv_url = "https://raw.githubusercontent.com/tuo-utente/tuo-repo/main/Chromateca_database.csv"

# Funzione per convertire ST_STABILITY in LED HTML
def stability_led(value):
    color_map = {'G': 'green', 'R': 'red', 'O': 'gold'}
    color = color_map.get(value, 'gray')
    return f"<div style='width:15px; height:15px; border-radius:50%; background:{color}; margin:auto'></div>"

try:
    df = pd.read_csv(csv_url, sep=";", engine="python", on_bad_lines="skip")

    # Filtro per TEXTURE
    if 'TEXTURE' in df.columns:
        texture_options = df['TEXTURE'].dropna().unique()
        selected_textures = st.multiselect("Filtra per TEXTURE", options=sorted(texture_options))

        if selected_textures:
            filtered_df = df[df['TEXTURE'].isin(selected_textures)]
        else:
            filtered_df = df
    else:
        filtered_df = df

    # Sostituisci ST_STABILITY con LED HTML
    if 'ST_STABILITY' in filtered_df.columns:
        df_display = filtered_df.copy()
        df_display['ST_STABILITY'] = df_display['ST_STABILITY'].apply(stability_led)
        st.markdown("<style>td {text-align: center !important;}</style>", unsafe_allow_html=True)
        st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Errore nel caricamento del file CSV: {e}")

