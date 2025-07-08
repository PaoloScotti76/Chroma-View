import streamlit as st
import pandas as pd

# Carica il file CSV
df = pd.read_csv("upgit.csv")

# Simula il contenuto HTML associato ai riferimenti CLOB
mock_html_content = {
    "oracle.sql.CLOB@1694d36d": "<h2>Immagine 1</h2><p>Segnaposto per immagine 1.</p>",
    "oracle.sql.CLOB@57e96b34": "<h2>Immagine 2</h2><p>Segnaposto per immagine 2.</p>"
}

# Titolo dell'app
st.title("Visualizzazione HTML da CSV")

# Mostra la tabella originale
st.subheader("Dati dal file CSV")
st.dataframe(df)

# Visualizza contenuti HTML simulati
st.subheader("Contenuti HTML simulati")
for index, row in df.iterrows():
    st.markdown(f"**ID:** {row['ID']}")
    html_content = mock_html_content.get(row["DISP_HTML"], "<p>Contenuto non disponibile</p>")
    st.markdown(html_content, unsafe_allow_html=True)
    st.markdown("---")
