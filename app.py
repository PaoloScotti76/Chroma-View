import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("BI Portfolio Mapping - Chromateca")

# URL del file CSV su GitHub (modificare con il proprio link raw)
csv_url = "Chromateca_database.csv"

@st.cache_data
def load_data():
    return pd.read_csv(csv_url, sep=";", engine="python", on_bad_lines="skip")

df = load_data()

# Filtri interattivi
with st.sidebar:
    st.header("Filtri")
    texture = st.multiselect("TEXTURE", sorted(df["TEXTURE"].dropna().unique()))
    typology = st.multiselect("TYPOLOGY", sorted(df["TYPOLOGY"].dropna().unique()))
    range_ = st.multiselect("RANGE", sorted(df["RANGE"].dropna().unique()))
    naturality = st.multiselect("NATURALITY", sorted(df["NATURALITY"].dropna().unique()))

filtered_df = df.copy()
if texture:
    filtered_df = filtered_df[filtered_df["TEXTURE"].isin(texture)]
if typology:
    filtered_df = filtered_df[filtered_df["TYPOLOGY"].isin(typology)]
if range_:
    filtered_df = filtered_df[filtered_df["RANGE"].isin(range_)]
if naturality:
    filtered_df = filtered_df[filtered_df["NATURALITY"].isin(naturality)]

# Scatter plot
st.subheader("Mappa a bolle")

numeric_options = ["LOW_VALUE", "MEDIUM_VALUE", "HIGH_VALUE", "SEMAFOTO_TALCO_COST"]
x_axis = st.selectbox("Asse X", numeric_options, index=0)
y_axis = st.selectbox("Asse Y", numeric_options, index=1)

fig, ax = plt.subplots(figsize=(10, 6))
palette = {"G": "green", "R": "red", "O": "gold", "Y": "gold"}

sns.scatterplot(
    data=filtered_df,
    x=x_axis,
    y=y_axis,
    size="HIGH_VALUE",
    hue="ST_STABILITY",
    palette=palette,
    sizes=(20, 300),
    alpha=0.7,
    ax=ax
)

plt.legend(title="ST_STABILITY", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig)

# Tabella dati
st.subheader("Dati filtrati")
st.dataframe(filtered_df, use_container_width=True)
