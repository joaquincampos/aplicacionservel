import pandas as pd
import unicodedata
import re
from fuzzywuzzy import process, fuzz

def normalize_string(s):
    # Normalizar acentos y caracteres especiales
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    # Convertir a minúsculas
    s = s.lower()
    # Reemplazar ñ por n
    s = s.replace('ñ', 'n')
    # Eliminar caracteres especiales
    s = re.sub(r'[^a-z0-9\s]', '', s)
    # Eliminar espacios extra
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# Cargar ambos archivos
df1 = pd.read_excel(r'D:\Documentos 2\Mapa Calor\establecimientos_educacionales_2021.xlsx')
df2 = pd.read_excel(r'D:\Documentos 2\Mapa Calor\locales_unicos_por_comuna.xlsx')

# Normalizar los nombres de las comunas y de los establecimientos para eliminar acentuación y otros caracteres
df1['NOM_COM_RB'] = df1['NOM_COM_RB'].apply(normalize_string)
df1['NOM_RBD'] = df1['NOM_RBD'].apply(normalize_string)
df2['Comuna'] = df2['Comuna'].apply(normalize_string)
df2['Local'] = df2['Local'].apply(normalize_string)

# Preparar un diccionario para los resultados
resultados = {}

# Lista para registrar los nombres de establecimientos ya emparejados
emparejados = []

# Iterar sobre cada comuna en el segundo archivo
for comuna in df2['Comuna'].unique():
    # Filtrar ambos DataFrames por la comuna actual
    establecimientos_df1 = df1[df1['NOM_COM_RB'] == comuna]['NOM_RBD'].tolist()
    locales_df2 = df2[df2['Comuna'] == comuna]['Local'].tolist()
    
    # Contadores para los encontrados y no encontrados
    encontrados = 0
    no_encontrados = []
    
    # Usar fuzzywuzzy para encontrar coincidencias de nombres de locales
    for local in locales_df2:
        # Encontrar la mejor coincidencia en la otra lista que aún no ha sido emparejada
        establecimientos_disponibles = [e for e in establecimientos_df1 if e not in emparejados]
        match = process.extractOne(local, establecimientos_disponibles, scorer=fuzz.token_set_ratio, score_cutoff=90)
        if match:
            encontrados += 1  # Incrementar contador de encontrados
            emparejados.append(match[0])  # Agregar la coincidencia a la lista de emparejados
        else:
            no_encontrados.append(local)  # Agregar al listado de no encontrados si no hay coincidencia
   
    # Guardar los resultados en el diccionario
    resultados[comuna] = {
        'total_encontrados': encontrados,
        'total_no_encontrados': len(no_encontrados),
        'locales_no_encontrados': no_encontrados
    }

# Convertir los resultados a un DataFrame para exportar a Excel
resultados_df = pd.DataFrame(
    [(k, v['total_encontrados'], v['total_no_encontrados'], v['locales_no_encontrados']) 
     for k, v in resultados.items()], 
    columns=['Comuna', 'Total Encontrados', 'Total No Encontrados', 'Locales No Encontrados']
)

# Guardar el DataFrame en un nuevo archivo Excel
resultados_df.to_excel(r'D:\Documentos 2\Mapa Calor\resultados_comparacion.xlsx', index=False)
