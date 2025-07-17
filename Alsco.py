import streamlit as st
from datetime import date
import pandas as pd
import smtplib
from email.message import EmailMessage
import tempfile
import os

st.title("Modulo di Rilevamento Difetti")

# Selezione articolo
articoli = ["Camice Oscar", "Giacca", "Pantaloni"]
articolo = st.selectbox("Codice articolo e tipo:", articoli)

# Selezione taglia
taglie = {
    "XXS": 1, "XS": 2, "S": 3, "M": 4, "L": 5, "XL": 6,
    "2XL": 7, "3XL": 8, "4XL": 9, "5XL": 10, "6XL": 11
}
taglia = st.selectbox("Taglia:", list(taglie.keys()))

# Data rilevamento
data_rilevamento = st.date_input("Data di rilevamento del difetto:", value=date.today())

# Responsabile
responsabile = st.text_input("Responsabile del rilevamento (Nome e Cognome):")

# ID Badge
id_badge = st.text_input("ID Badge:")

# Codice a barre
codice_barre = st.text_input("Codice a barre del capo:")

# Difetti
difetti = [
    "Macchie - colletto", "Macchie - maniche", "Macchie - polsini", "Macchie - tronco",
    "Scuciture - orlo", "Scuciture - laterali", "Scuciture - patta", "Scuciture - bordo interna", "Scuciture - tasca", "Scuciture - manica",
    "Bottoni a pressione non si chiudono - frontali", "Bottoni a pressione non si chiudono - polsini", "Bottoni a pressione non si chiudono - in vita",
    "Bottoni a pressione non si chiudono - patta", "Bottoni a pressione non si chiudono - stringivita", "Bottoni a pressione non si chiudono - alla caviglia",
    "Bottoni rotti - polsini", "Bottoni rotti - in vita", "Bottoni rotti - stringivita", "Bottoni rotti - alla caviglia"
]
difetto = st.selectbox("Tipo di difetto:", difetti)

# Localizzazione
localizzazioni = ["anteriore", "posteriore", "interna", "sul petto", "sul fianco", "dx", "sx", "dx laterale", "sx posteriore"]
localizzazione = st.selectbox("Localizzazione del difetto:", localizzazioni)

# Configurazione SMTP
st.markdown("### Configurazione SMTP")
smtp_server = st.text_input("SMTP Server", value="smtp.chromavis.com")
smtp_port = st.number_input("SMTP Port", value=587)
smtp_user = st.text_input("SMTP Username", value="noreply@chromavis.com")
smtp_password = st.text_input("SMTP Password", type="password")

# Invio
if st.button("Invia segnalazione via email"):
    df = pd.DataFrame([{
        "Articolo": articolo,
        "Taglia": taglia,
        "Codice Taglia": taglie[taglia],
        "Data Rilevamento": data_rilevamento,
        "Responsabile": responsabile,
        "ID Badge": id_badge,
        "Codice a Barre": codice_barre,
        "Difetto": difetto,
        "Localizzazione": localizzazione
    }])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        excel_path = tmp.name
        df.to_excel(excel_path, index=False)

    msg = EmailMessage()
    msg['Subject'] = 'Segnalazione Difetto'
    msg['From'] = smtp_user
    msg['To'] = 'paolo.scotti@chromavis.com'
    msg.set_content('In allegato la segnalazione del difetto rilevato.')

    with open(excel_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application",
                           subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           filename="segnalazione.xlsx")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        st.success("Email inviata con successo a paolo.scotti@chromavis.com")
    except Exception as e:
        st.error(f"Errore durante l'invio dell'email: {e}")
    finally:
        os.remove(excel_path)
