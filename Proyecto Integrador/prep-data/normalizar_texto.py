import pandas as pd
from unidecode import unidecode

# Función para normalizar texto
def normalizar_texto(texto):
    if pd.isna(texto):  # Manejar valores nulos
        return ""
    texto = unidecode(str(texto).lower())  # Convertir a minúsculas y eliminar tildes
    texto = texto.replace(",", "").replace(".", "")  # Quitar puntuaciones
    palabras_irrelevantes = ["de", "la", "el", "las", "los", "vereda", "municipio", "-"]  # Lista de palabras comunes
    texto = " ".join([palabra for palabra in texto.split() if palabra not in palabras_irrelevantes])
    return texto

# Método principal que retorna el dataset con columnas nuevas
def agregar_columnas_normalizadas(ruta_dataset):
    # Cargar el dataset
    original_df = pd.read_csv(ruta_dataset,
                          delimiter=',', 
                          dtype=str, 
                          low_memory=False, 
                          encoding='utf-8')  # Omitir líneas en blanco

    
    # Normalizar las columnas requeridas
    original_df["Municipio_normalizado"] = original_df["Municipio de residencia (PcD)"].apply(normalizar_texto)
    original_df["BarrioVereda_normalizado"] = original_df["Nombre del Barrio o Vereda (PcD)"].apply(normalizar_texto)
    
    # Retornar el DataFrame actualizado
    return original_df

def get_municipio_normalizado(row):
    return row["Municipio_normalizado"]

def get_vereda_normalizada(row):
    return row["BarrioVereda_normalizado"]

# Método para verificar si el municipio pertenece al Área Metropolitana
def verificar_area_metropolitana(row):
    # Nombres de los municipios del área metropolitana normalizados
    area_metropolitana = [
    "barbosa", "girardota", "copacabana", "bello", "medellin",
    "itagui", "sabaneta", "envigado", "la estrella", "caldas"]

    return row["Municipio_normalizado"] in area_metropolitana

# Guardar el dataset actualizado (opcional)
#dataset_actualizado.to_csv("../clean_pcd_data_normalizado.csv", index=False, encoding='utf-8', sep=';')