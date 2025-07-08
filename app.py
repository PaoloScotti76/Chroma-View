import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Visualizzatore Chromateca")

# URL del file CSV su GitHub
csv_url = "Chromateca_database.csv"

# Funzione per convertire valori in LED HTML
def led_indicator(value):
    color_map = {'G': 'green', 'R': 'red', 'O': 'gold', 'Y': 'gold'}
    color = color_map.get(str(value).strip().upper(), 'gray')
    return f"<div style='width:15px; height:15px; border-radius:50%; background:{color}; margin:auto'></div>"

# Colonne da convertire in LED
led_columns = [
    'ST_STABILITY',
    'ST_COMPATIBILITY',
    'SEMAFORO_INDUSTRIALIZZAZIONE',
    'ST_SAMPLING',
    'ST_SAMPLING_STOCK',
    'ST_SAFETY_TEST',
    'ST_IMERYS_TALC',
    'SEMAFOTO_TALCO_COST',
    'SEMAFORO_TEC_TRANSFER'
]

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

    # Sostituisci le colonne LED con HTML
    df_display = filtered_df.copy()
    for col in led_columns:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(led_indicator)

    # Visualizza la tabella con LED
    st.markdown("<style>td {text-align: center !important;}</style>", unsafe_allow_html=True)
    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

except Exception as e:
    st.error(f"Errore nel caricamento del file CSV: {e}")

