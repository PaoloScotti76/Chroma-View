import streamlit as st
import streamlit.components.v1 as components
import smtplib
from email.mime.text import MIMEText
from datetime import date


# Aggiunta del logo centrato
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://github.com/PaoloScotti76/Chroma-View/logo.png' width='200'>
    </div>
    """,
    unsafe_allow_html=True
)


# Titolo con font ridotto
st.markdown("<h4>Modulo Segnalazione Problemi/Difetti - ALSCO</h4>", unsafe_allow_html=True)

# 1. Codice articolo
codice_articolo = st.selectbox("Codice Articolo", [" ",
    "C0015175 – Camice Oscar Chromavis C/Tasche C/Elastico e Bottoni Polsi SBM Bianco",
    "C0015176 – Giacca Chromavis C/Tasca Int. C/Elastico e Bottoni Polsi Ecru",
    "C0015177 Pantalone Chromavis Evan – CHR C/Reg. Fondo SBM Ecru",
    "C0015178 – Giacca Ariel Chromavis C/Tasche C/Bottoni SBM Charcoal/Ecru",
    "C0015179 – Pantalone Evan Chromavis C/Tasche C/reg. Fondo SBM Charcoal/Ecru"
])

# 2. Taglia
taglia = st.selectbox("Selezione Taglia", [" ","XXS - 1", "XS - 2", "S - 3", "M - 4", "L - 5", "XL - 6", "2XL - 7", "3XL - 8", "4XL - 9", "5XL - 10", "6XL - 11"])

# 3. Data rilevamento
data_rilevamento = st.date_input("Data di rilevamento del difetto", value=date.today())

# 4. Responsabile
st.subheader("Responsabile del rilevamento")
nome_cognome = st.text_input("Nome e Cognome")
id_badge = st.text_input("ID Badge")
codice_barre = st.text_input("Codice a Barre del Capo (Se leggibile)")

# 5. Difetto
difetto = st.selectbox("Difetto/Problema", [" ","Macchie", "Scuciture", "Bottoni a pressione non si chiudono", "Bottoni Rotti"])

# 6. Localizzazione
localizzazione = st.selectbox("Localizzazione del difetto", [" ", "Anteriore", "Posteriore", "Interna", "Petto", "Fianco dx", "Fianco sx", "Laterale dx", "Laterale sx"])

# 7. Credito non disponibile
credito_non_disponibile = st.checkbox("Credito non disponibile")

# 8. Richieste specifiche
richieste_specifiche = st.text_area("Richieste specifiche")

# 9. Informazioni aggiuntive
informazioni_aggiuntive = st.text_area("Informazioni aggiuntive")

# Funzione invio email
def invia_email(corpo_email):
    mittente = "chromavis.alsco@gmail.com"
    destinatari = ["silvia.casagrande@chromavis.com"]
    oggetto = "ALSCO - Segnalazione problemi/difetti"

    msg = MIMEText(corpo_email)
    msg["Subject"] = oggetto
    msg["From"] = mittente
    msg["To"] = ", ".join(destinatari)

    try:
        with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
            server.starttls()
            server.login("926aa8001@smtp-brevo.com", "c9kDXBaMtPIgSHOx")
            server.sendmail(mittente, destinatari, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Errore nell'invio dell'email: {e}")
        return False

# Bottone invio
if st.button("Invia Segnalazione"):
    corpo = f"""
Segnalazione Problemi/Difetti - ALSCO

Codice Articolo: {codice_articolo}
Taglia: {taglia}
Data rilevamento: {data_rilevamento}

Responsabile:
- Nome e Cognome: {nome_cognome}
- ID Badge: {id_badge}
- Codice a Barre: {codice_barre}

Difetto/Problema: {difetto}
Localizzazione: {localizzazione}
Credito non disponibile: {"Sì" if credito_non_disponibile else "No"}

Richieste specifiche:
{richieste_specifiche}

Informazioni aggiuntive:
{informazioni_aggiuntive}
"""
    if invia_email(corpo):
        st.success("Segnalazione inviata con successo!")
