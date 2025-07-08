import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Excel file
excel_file = "Chromateca_15.10.xlsx"
df = pd.read_excel(excel_file, sheet_name="Chromateca_database_021024", engine="openpyxl")

# Set Streamlit page configuration
st.set_page_config(page_title="Texture Selection Dashboard", layout="wide")

# Title and description
st.title("✨ Texture Selection Dashboard")
st.markdown("Replicating Power BI layout with filters and charts")

# Sidebar filters
st.sidebar.header("🔍 Filters")

texture_status = st.sidebar.multiselect(
    "Texture Status",
    options=df["SEMAFORO_TEC_TRANSFER"].dropna().unique(),
    default=df["SEMAFORO_TEC_TRANSFER"].dropna().unique()
)

portfolio = st.sidebar.multiselect(
    "Portfolio Mapping",
    options=df["COLLECTION"].dropna().unique(),
    default=df["COLLECTION"].dropna().unique()
)

texture_profile = st.sidebar.multiselect(
    "Texture Profile",
    options=df["DESCRIPTOR"].dropna().unique(),
    default=df["DESCRIPTOR"].dropna().unique()
)

sample_location = st.sidebar.multiselect(
    "Sample Location",
    options=df["PLANT"].dropna().unique(),
    default=df["PLANT"].dropna().unique()
)

# Apply filters
filtered_df = df[
    (df["SEMAFORO_TEC_TRANSFER"].isin(texture_status)) &
    (df["COLLECTION"].isin(portfolio)) &
    (df["DESCRIPTOR"].isin(texture_profile)) &
    (df["PLANT"].isin(sample_location))
]

# Layout with columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Texture Status Distribution")
    fig1 = px.histogram(filtered_df, x="SEMAFORO_TEC_TRANSFER", color="SEMAFORO_TEC_TRANSFER")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📦 Portfolio Mapping")
    fig2 = px.histogram(filtered_df, x="COLLECTION", color="COLLECTION")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("🧪 Texture Profile")
    fig3 = px.histogram(filtered_df, x="DESCRIPTOR", color="DESCRIPTOR")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🏭 Sample Location")
    fig4 = px.histogram(filtered_df, x="PLANT", color="PLANT")
    st.plotly_chart(fig4, use_container_width=True)

# Show filtered data
with st.expander("📄 Show Filtered Data"):
    st.dataframe(filtered_df)


