import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import date

if "reset_form" in st.session_state and st.session_state.reset_form:
    resettable_keys = [
        "codice_articolo", "taglia", "data_rilevamento", "nome_cognome",
        "id_badge", "codice_barre", "difetto", "localizzazione",
        "credito_non_disponibile", "richieste_specifiche", "informazioni_aggiuntive"
    ]
    for key in resettable_keys:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.reset_form = False

def reset_form():
    st.session_state.reset_form = True
    st.rerun()

st.image("logo.png", use_container_width=False)
st.markdown("<h4>Modulo Segnalazione Problemi/Difetti - ALSCO</h4>", unsafe_allow_html=True)

codice_articolo = st.selectbox("Codice Articolo", [" ",
    "C0015175 – Camice Oscar Chromavis C/Tasche C/Elastico e Bottoni Polsi SBM Bianco",
    "C0015176 – Giacca Chromavis C/Tasca Int. C/Elastico e Bottoni Polsi Ecru",
    "C0015177 Pantalone Chromavis Evan – CHR C/Reg. Fondo SBM Ecru",
    "C0015178 – Giacca Ariel Chromavis C/Tasche C/Bottoni SBM Charcoal/Ecru",
    "C0015179 – Pantalone Evan Chromavis C/Tasche C/reg. Fondo SBM Charcoal/Ecru"
], key="codice_articolo")

taglia = st.selectbox("Selezione Taglia", [" ","XXS - 1", "XS - 2", "S - 3", "M - 4", "L - 5", "XL - 6", "2XL - 7", "3XL - 8", "4XL - 9", "5XL - 10", "6XL - 11"], key="taglia")

data_rilevamento = st.date_input("Data di rilevamento del difetto", value=date.today(), key="data_rilevamento")

st.subheader("Responsabile del rilevamento")
nome_cognome = st.text_input("Nome e Cognome", key="nome_cognome")
id_badge = st.text_input("ID Badge", key="id_badge")
codice_barre = st.text_input("Codice a Barre del Capo (Se leggibile)", key="codice_barre")

difetto = st.selectbox("Difetto/Problema", [" ","Macchie", "Scuciture", "Bottoni a pressione non si chiudono", "Bottoni Rotti"], key="difetto")

localizzazione = st.selectbox("Localizzazione del difetto", [" ", "Anteriore", "Posteriore", "Interna", "Petto", "Fianco dx", "Fianco sx", "Laterale dx", "Laterale sx"], key="localizzazione")

credito_non_disponibile = st.checkbox("Credito non disponibile", key="credito_non_disponibile")

richieste_specifiche = st.text_area("Richieste specifiche", key="richieste_specifiche")

informazioni_aggiuntive = st.text_area("Informazioni aggiuntive", key="informazioni_aggiuntive")

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

col1, col2 = st.columns([1, 1])

with col1:
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
            reset_form()

with col2:
    if st.button("Refresh"):    
        reset_form()

