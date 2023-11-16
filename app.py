import streamlit as st
import pandas as pd
import geopandas as gpd

st.title("Aplicación datos SERVEL")
df = pd.read_parquet("./datos/datos_servel_2022.parquet")
st.dataframe(df.head())
colegios = gpd.read_file("./datos/Establecimientos Educacionales 2021/Establecimientos_Educacionales_2021.shp")
st.write(colegios.head())


    