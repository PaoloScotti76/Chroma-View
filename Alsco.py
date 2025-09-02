import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import date

def force_reset():
    st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)

st.image("logo.png", use_container_width=False)
st.markdown("<h4>Modulo Segnalazione Problemi/Difetti - ALSCO</h4>", unsafe_allow_html=True)

if "submitted" not in st.session_state:
    st.session_state.submitted = False

with st.form(key="segnalazione_form"):
    codice_articolo = st.selectbox("Codice Articolo", [" ",
        "C0015175 – Camice Oscar Chromavis",
        "C0015176 – Giacca Chromavis",
        "C0015177 – Pantalone Chromavis",
        "C0015178 – Giacca Ariel Chromavis",
        "C0015179 – Pantalone Evan Chromavis"
    ])

    taglia = st.selectbox("Selezione Taglia", [" ","XXS - 1", "XS - 2", "S - 3", "M - 4", "L - 5"])
    data_rilevamento = st.date_input("Data di rilevamento", value=date.today())

    st.subheader("Responsabile del rilevamento")
    nome_cognome = st.text_input("Nome e Cognome")
    id_badge = st.text_input("ID Badge")
    codice_barre = st.text_input("Codice a Barre")

    difetto = st.selectbox("Difetto", [" ","Macchie", "Scuciture", "Bottoni rotti"])
    localizzazione = st.selectbox("Localizzazione", [" ", "Anteriore", "Posteriore"])
    credito_non_disponibile = st.checkbox("Credito non disponibile")
    richieste_specifiche = st.text_area("Richieste specifiche")
    informazioni_aggiuntive = st.text_area("Informazioni aggiuntive")

    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Invia Segnalazione")
    with col2:
        reset = st.form_submit_button("Refresh")

if submit:
    corpo = f"""
Segnalazione Problemi/Difetti - ALSCO

Codice Articolo: {codice_articolo}
Taglia: {taglia}
Data rilevamento: {data_rilevamento}

Responsabile:
- Nome e Cognome: {nome_cognome}
- ID Badge: {id_badge}
- Codice a Barre: {codice_barre}

Difetto: {difetto}
Localizzazione: {localizzazione}
Credito non disponibile: {"Sì" if credito_non_disponibile else "No"}

Richieste specifiche:
{richieste_specifiche}

Informazioni aggiuntive:
{informazioni_aggiuntive}
"""
    try:
        mittente = "chromavis.alsco@gmail.com"
        destinatari = ["silvia.casagrande@chromavis.com,d.lanoce@alsco.it,d.cavalli@alsco.it"]
        oggetto = "ALSCO - Segnalazione problemi/difetti"

        msg = MIMEText(corpo)
        msg["Subject"] = oggetto
        msg["From"] = mittente
        msg["To"] = ", ".join(destinatari)

        with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
            server.starttls()
            server.login("926aa8001@smtp-brevo.com", "c9kDXBaMtPIgSHOx")
            server.sendmail(mittente, destinatari, msg.as_string())

        st.success("Segnalazione inviata con successo!")
        st.session_state.submitted = True

    except Exception as e:
        st.error(f"Errore nell'invio dell'email: {e}")

if reset:
    force_reset()

