import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static
import folium


@st.cache_data
def leer_datos():
    df = pd.read_parquet("./datos/datos_servel_2022.parquet")
    colegios = gpd.read_file("./datos/Establecimientos Educacionales 2021/Establecimientos_Educacionales_2021.shp")
    return df, colegios


def main():
    st.title("Aplicación datos SERVEL")
    df, colegios = leer_datos()
    st.dataframe(df.head())
    # Visualizar los primeros registros de los datos de colegios
    st.write(colegios.head())
    mapping(colegios.sample(100))


def mapping(colegios: gpd.GeoDataFrame):
    # Crear un mapa centrado en Chile
    m = folium.Map(location=[-35, -70], zoom_start=5)

    # Añadir los colegios como círculos al mapa
    for idx, row in colegios.iterrows():
        # Asegúrate de usar el nombre correcto de la columna
        folium.CircleMarker(
            location=[row['LATITUD'], row['LONGITUD']],
            radius=2,  # Tamaño del círculo
            color='red',  # Color del círculo
            fill=True,
            fill_color='red'  # Relleno del círculo
        ).add_to(m)

    # Mostrar el mapa en la aplicación
    folium_static(m)


main()







    