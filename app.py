import streamlit as st
import pandas as pd
st.title("Aplicación datos SERVEL")
df = pd.read_parquet("./datos/datos_servel_2022.parquet")
st.dataframe(df)